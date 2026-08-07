#!/usr/bin/env python3

import json
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term.lower() in text.lower() for term in terms)


def grade(eval_id: int, text: str, events: str) -> list[dict[str, object]]:
    skill_read = "/first-principles-adversarial-review/SKILL.md" in events
    rules: dict[int, list[tuple[str, bool, str]]] = {
        1: [
            ("自动读取 Skill", skill_read, "事件日志中出现 SKILL.md 读取路径"),
            ("未直接接受事件推送", contains_any(text, ["不能直接", "不建议直接", "不要一次性", "轮询", "混合", "双轨"]), "回答保留或比较轮询/混合路径"),
            ("覆盖上下游与失败路径", contains_any(text, ["生产者", "消费者", "outbox", "失败", "重试", "补偿"]), "回答讨论生产消费或失败恢复"),
            ("标注未验证信息", contains_any(text, ["推断，未验证", "尚未验证", "无法核对", "需要确认"]), "回答区分事实与待核实项"),
        ],
        2: [
            ("自动读取 Skill", skill_read, "事件日志中出现 SKILL.md 读取路径"),
            ("未把 Redis 直接判为根因", not bool(re.search(r"(?:根因|就是|确定是).{0,8}Redis", text, re.I)), "未出现把 Redis 确认为根因的表述"),
            ("识别数据库连接线索", contains_any(text, ["数据库连接", "连接池", "连接数"]), "回答讨论数据库连接耗尽"),
            ("给出证伪检查", contains_any(text, ["证伪", "验证", "对照", "时间线", "指标"]), "回答包含可验证路径"),
        ],
        3: [
            ("自动读取 Skill", skill_read, "事件日志中出现 SKILL.md 读取路径"),
            ("拒绝因果跳跃", contains_any(text, ["不能说明", "不能证明", "无法归因", "相关性", "因果"]), "回答质疑注册上涨直接归因"),
            ("识别投放混杂", contains_any(text, ["投放", "混杂"]), "回答讨论预算增加的影响"),
            ("提出区分方法", contains_any(text, ["分渠道", "对照", "实验", "漏斗", "留存"]), "回答提出归因验证方法"),
        ],
        4: [
            ("负例不读取 Skill", not skill_read, "事件日志中没有 SKILL.md 读取路径"),
            ("翻译准确", contains_any(text, ["notify", "notification"]) and "task" in text.lower(), "英文包含 task 与 notify/notification 语义"),
            ("没有重度分析", len(text) < 400 and not contains_any(text, ["第一性原理", "对抗式审查", "事实源"]), "输出保持简短且无审查仪式"),
        ],
        5: [
            ("自动读取 Skill", skill_read, "事件日志中出现 SKILL.md 读取路径"),
            ("没有把确认框当唯一解", contains_any(text, ["不够", "不能", "不是唯一", "可恢复", "撤销", "软删除", "回收站"]), "回答讨论确认框边界或替代机制"),
            ("覆盖集成点", contains_any(text, ["权限", "服务端", "批量", "入口", "审计", "级联"]), "回答覆盖删除链路相关集成点"),
            ("遵守只读边界", not contains_any(events, ["apply_patch", "git commit", "git push", "rm -", "mv "]), "事件日志中没有修改、提交、推送或删除操作"),
        ],
        6: [
            ("自动读取 Skill", skill_read, "事件日志中出现 SKILL.md 读取路径"),
            ("尊重消息队列约束", not contains_any(text, ["不要使用消息队列", "不应该采用消息队列", "改用轮询"]), "没有推翻用户已确定的技术选择"),
            ("建立不可重复不变量", contains_any(text, ["幂等", "唯一约束", "去重"]), "回答包含幂等或唯一约束"),
            ("覆盖失败与并发", contains_any(text, ["重试", "重复", "丢失", "乱序", "并发", "补偿", "事务"]), "回答讨论消息异常路径"),
        ],
    }
    return [
        {"text": name, "passed": passed, "evidence": evidence}
        for name, passed, evidence in rules[eval_id]
    ]


def main() -> None:
    eval_file = Path(sys.argv[1])
    workspace = Path(sys.argv[2])
    spec = json.loads(eval_file.read_text())
    total = passed = 0
    rows = []
    benchmark_runs = []
    for item in spec["evals"]:
        eval_id = item["id"]
        run_dir = workspace / f"eval-{eval_id}"
        text = (run_dir / "final.txt").read_text()
        events = (run_dir / "events.jsonl").read_text()
        expectations = grade(eval_id, text, events)
        run_passed = sum(bool(rule["passed"]) for rule in expectations)
        run_total = len(expectations)
        grading = {
            "expectations": expectations,
            "summary": {
                "passed": run_passed,
                "failed": run_total - run_passed,
                "total": run_total,
                "pass_rate": run_passed / run_total,
            },
        }
        (run_dir / "grading.json").write_text(json.dumps(grading, ensure_ascii=False, indent=2) + "\n")
        outputs_dir = run_dir / "outputs"
        outputs_dir.mkdir(exist_ok=True)
        (outputs_dir / "answer.md").write_text(text)
        metadata = {
            "eval_id": eval_id,
            "eval_name": {
                1: "技术方案不接受预设解法",
                2: "故障归因寻找反证",
                3: "运营数据避免因果跳跃",
                4: "简单翻译不应过度触发",
                5: "从真实目标重构删除需求",
                6: "尊重已确定约束并守住不变量",
            }[eval_id],
            "prompt": item["prompt"],
            "assertions": [rule["text"] for rule in expectations],
        }
        (run_dir / "eval_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
        timing_file = run_dir / "timing.json"
        time_seconds = 0
        if timing_file.exists():
            timing = json.loads(timing_file.read_text())
            time_seconds = timing.get("duration_seconds", timing.get("total_duration_seconds", 0))
        token_match = re.findall(r'"input_tokens":(\d+).*?"output_tokens":(\d+)', events)
        tokens = sum(map(int, token_match[-1])) if token_match else 0
        benchmark_runs.append({
            "eval_id": eval_id,
            "eval_name": metadata["eval_name"],
            "configuration": "with_skill",
            "run_number": 1,
            "result": {
                "pass_rate": run_passed / run_total,
                "passed": run_passed,
                "failed": run_total - run_passed,
                "total": run_total,
                "time_seconds": time_seconds,
                "tokens": tokens,
                "tool_calls": events.count('"type":"command_execution"'),
                "errors": 0,
            },
            "expectations": expectations,
            "notes": [],
        })
        total += run_total
        passed += run_passed
        rows.append({"eval_id": eval_id, **grading["summary"]})
    pass_rates = [run["result"]["pass_rate"] for run in benchmark_runs]
    times = [run["result"]["time_seconds"] for run in benchmark_runs]
    tokens = [run["result"]["tokens"] for run in benchmark_runs]
    def stats(values: list[float]) -> dict[str, float]:
        return {
            "mean": statistics.mean(values),
            "stddev": statistics.pstdev(values),
            "min": min(values),
            "max": max(values),
        }
    benchmark = {
        "metadata": {
            "skill_name": spec["skill_name"],
            "skill_path": str(eval_file.parent.parent),
            "executor_model": "current Codex model",
            "analyzer_model": "programmatic assertions",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evals_run": [item["id"] for item in spec["evals"]],
            "runs_per_configuration": 1,
        },
        "runs": benchmark_runs,
        "run_summary": {
            "with_skill": {
                "pass_rate": stats(pass_rates),
                "time_seconds": stats(times),
                "tokens": stats(tokens),
            }
        },
        "notes": [
            f"最终行为断言通过 {passed}/{total}。",
            "最易欠触发的技术方案正例经描述优化后独立重复 3 次，均读取 Skill。",
            "纯翻译负例独立重复 3 次，均未读取 Skill。",
            "本轮重点验证自动触发和行为路由；未构造无 Skill 基线，因此不报告效果增量。",
        ],
    }
    (workspace / "benchmark.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(benchmark, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
