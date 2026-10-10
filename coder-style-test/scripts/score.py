import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "references" / "coder-style.json"
SITE = "https://kakarot-index.kakarot-space.workers.dev/coder-style/"


def main() -> None:
    parser = argparse.ArgumentParser(description="按 20 道题的答案计算编程风格")
    parser.add_argument("answers", help="按题号顺序的 A/B 答案，例如 ABBAABABBAABABBAABAB；空格和逗号会被忽略")
    args = parser.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    axes, questions, types = data["axes"], data["questions"], data["types"]
    answers = [c for c in args.answers.upper() if c not in " ,，"]
    if len(answers) != len(questions) or any(c not in "AB" for c in answers):
        raise SystemExit(f"答案必须是 {len(questions)} 个 A 或 B，当前收到 {len(answers)} 个：{''.join(answers)}")

    per_axis = len(questions) // len(axes)
    scores = []
    code = ""
    for axis in axes:
        first, second = list(axis["poles"])
        count = sum(
            1
            for question, answer in zip(questions, answers)
            if question["axis"] == axis["id"] and question["options"][0 if answer == "A" else 1]["pole"] == first
        )
        scores.append(count)
        code += first if count * 2 > per_axis else second

    style = types[code]
    partner = types[style["partner"]]
    lines = [
        f"# {code} · {style['name']}（{style['en']}）",
        "",
        f"> {style['tagline']}",
        "",
        style["desc"],
        "",
        "## 四个方面",
        "",
        "| 方面 | 倾向 | 比例 |",
        "|---|---|---|",
    ]
    for axis, count in zip(axes, scores):
        first, second = axis["poles"].values()
        percent = round(count / per_axis * 100)
        lean = first if percent >= 50 else second
        lines.append(f"| {axis['title']} | {lean['name']}：{lean['hint']} | {first['name']} {percent}% · {second['name']} {100 - percent}% |")
    lines += [
        "",
        "## 你的强项",
        "",
        *[f"- {text}" for text in style["strengths"]],
        "",
        "## 要留意的地方",
        "",
        style["blindspot"],
        "",
        "## 和 Agent 合作的建议",
        "",
        style["agentTip"],
        "",
        f"最互补的搭档：**{partner['name']} {style['partner']}**，{partner['tagline']}",
        "",
        f"网页版结果（可分享）：{SITE}#r={''.join(map(str, scores))}",
    ]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
