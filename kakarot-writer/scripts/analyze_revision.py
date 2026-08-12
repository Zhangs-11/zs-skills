#!/usr/bin/env python3
"""Compare a delivered draft with the author's final text without inventing preferences."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[\u4e00-\u9fff]|[A-Za-z0-9_]+|[^\s]")
MARKERS = {
    "不是…而是…": re.compile(r"不是.{0,40}而是"),
    "与其说…不如说…": re.compile(r"与其说.{0,40}不如说"),
    "先说结论": re.compile(r"先说结论|我先把结论放这"),
    "冒号": re.compile(r"[：:]"),
    "破折号": re.compile(r"—|–"),
    "问号": re.compile(r"[？?]"),
    "感叹号": re.compile(r"[！!]"),
    "第一人称": re.compile(r"我|我们"),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def metrics(text: str) -> dict[str, int]:
    return {
        "characters": len(re.sub(r"\s", "", text)),
        "paragraphs": len(paragraphs(text)),
        "single_sentence_paragraphs": sum(
            1 for paragraph in paragraphs(text) if len(re.findall(r"[。！？!?]", paragraph)) <= 1
        ),
        **{label: len(pattern.findall(text)) for label, pattern in MARKERS.items()},
    }


def changed_blocks(draft: str, final: str, limit: int = 20) -> list[dict[str, object]]:
    draft_parts = paragraphs(draft)
    final_parts = paragraphs(final)
    matcher = difflib.SequenceMatcher(a=draft_parts, b=final_parts, autojunk=False)
    blocks: list[dict[str, object]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        blocks.append(
            {
                "change": tag,
                "draft_paragraphs": [i1 + 1, i2],
                "final_paragraphs": [j1 + 1, j2],
                "draft": draft_parts[i1:i2],
                "final": final_parts[j1:j2],
            }
        )
        if len(blocks) >= limit:
            break
    return blocks


def token_changes(draft: str, final: str, limit: int = 30) -> dict[str, list[list[object]]]:
    draft_counts = Counter(tokens(draft))
    final_counts = Counter(tokens(final))
    removed = draft_counts - final_counts
    added = final_counts - draft_counts
    return {
        "removed": [[token, count] for token, count in removed.most_common(limit)],
        "added": [[token, count] for token, count in added.most_common(limit)],
    }


def build_report(draft: str, final: str, draft_path: Path, final_path: Path) -> dict[str, object]:
    draft_metrics = metrics(draft)
    final_metrics = metrics(final)
    return {
        "schema_version": 1,
        "sources": {"draft": str(draft_path), "final": str(final_path)},
        "similarity": round(difflib.SequenceMatcher(a=draft, b=final, autojunk=False).ratio(), 4),
        "metrics": {
            "draft": draft_metrics,
            "final": final_metrics,
            "delta": {key: final_metrics[key] - draft_metrics[key] for key in draft_metrics},
        },
        "token_changes": token_changes(draft, final),
        "changed_blocks": changed_blocks(draft, final),
        "interpretation_boundary": (
            "本报告只陈述文本差异，不自动证明作者偏好。事实修正、篇幅限制、平台要求和本篇策略"
            "都可能造成相同改动；必须结合上下文审查并经作者确认后才能更新长期规则。"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="Agent 交付给作者的初稿")
    parser.add_argument("final", type=Path, help="作者确认后的终稿")
    parser.add_argument("--output", type=Path, required=True, help="写入 JSON 差异报告的路径")
    args = parser.parse_args()
    report = build_report(read_text(args.draft), read_text(args.final), args.draft, args.final)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"差异报告已生成：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
