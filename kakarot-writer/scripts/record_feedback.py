#!/usr/bin/env python3
"""Record one writing feedback event without publishing private article content."""

from __future__ import annotations

import argparse
import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path


CATEGORIES = {"deterministic_error", "style_candidate", "one_off_choice", "unknown"}
OWNERS = {"kakarot-writer", "wechat-publisher", "visual-workflow", "unknown"}
STATUSES = {"hard_rule", "candidate", "one_off", "needs_review"}
FIXED_STATUS = {
    "deterministic_error": "hard_rule",
    "one_off_choice": "one_off",
    "unknown": "needs_review",
}
MAX_EVIDENCE_CHARS = 500
MAX_FIELD_CHARS = 500


def build_event(
    *,
    article_id: str,
    summary: str,
    correction: str,
    category: str,
    owner: str,
    status: str,
    scope: str,
    evidence: list[str] | None = None,
    counterevidence: list[str] | None = None,
    independent_article_ids: list[str] | None = None,
    explicit_long_term_instruction: bool = False,
    author_confirmed: bool = False,
) -> dict[str, object]:
    if category not in CATEGORIES:
        raise ValueError(f"unsupported category: {category}")
    if owner not in OWNERS:
        raise ValueError(f"unsupported owner: {owner}")
    if status not in STATUSES:
        raise ValueError(f"unsupported status: {status}")
    for label, value in (
        ("article_id", article_id),
        ("summary", summary),
        ("correction", correction),
        ("scope", scope),
    ):
        if not value.strip() or len(value) > MAX_FIELD_CHARS:
            raise ValueError(f"{label} must be a non-empty redacted summary no longer than 500 characters")
    if category != "style_candidate" and (explicit_long_term_instruction or author_confirmed):
        raise ValueError(
            "explicit_long_term_instruction and author_confirmed apply only to style_candidate"
        )
    required_status = FIXED_STATUS.get(category)
    if required_status and status != required_status:
        raise ValueError(f"{category} must use status={required_status}")
    article_ids = sorted({article_id, *(independent_article_ids or [])})
    evidence_items = evidence or []
    counterevidence_items = counterevidence or []
    if sum(len(item) for item in evidence_items + counterevidence_items) > MAX_EVIDENCE_CHARS:
        raise ValueError("all evidence must fit a 500-character redacted-summary budget")
    if category == "style_candidate" and status == "hard_rule":
        confirmed_recurrence = author_confirmed and len(article_ids) >= 2
        if not explicit_long_term_instruction and not confirmed_recurrence:
            raise ValueError(
                "style_candidate cannot become a hard_rule without an explicit long-term "
                "instruction, or two independent articles followed by author confirmation"
            )
    if category == "style_candidate" and status not in {"candidate", "hard_rule"}:
        raise ValueError("style_candidate must use status=candidate or status=hard_rule")
    return {
        "schema_version": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "article_id": article_id,
        "summary": summary,
        "correction": correction,
        "category": category,
        "owner": owner,
        "status": status,
        "scope": scope,
        "evidence": evidence_items,
        "counterevidence": counterevidence_items,
        "independent_article_ids": article_ids,
        "recurrence_count": len(article_ids),
        "explicit_long_term_instruction": explicit_long_term_instruction,
        "author_confirmed": author_confirmed,
        "regression_test_required": category == "deterministic_error",
        "privacy": "private_task_artifact_do_not_commit",
    }


def resolve_output_path(
    output: Path | None,
    *,
    article_id: str,
    allow_repository_output: bool = False,
) -> Path:
    if output is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        safe_article_id = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in article_id)
        unique = uuid.uuid4().hex[:12]
        return (
            Path(tempfile.gettempdir())
            / "kakarot-writing-feedback"
            / safe_article_id
            / f"{timestamp}-{unique}.json"
        )
    resolved = output.expanduser().resolve()
    if not allow_repository_output and _inside_git_worktree(resolved):
        raise ValueError(
            "refusing to write private feedback inside a Git worktree; omit --output to use "
            "the private temporary location"
        )
    return resolved


def _inside_git_worktree(path: Path) -> bool:
    current = path if path.is_dir() else path.parent
    return any((parent / ".git").exists() for parent in (current, *current.parents))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--article-id", required=True)
    parser.add_argument("--summary", required=True, help="错误或偏好候选的简短描述")
    parser.add_argument("--correction", required=True, help="正确规则或本次修改")
    parser.add_argument("--category", choices=sorted(CATEGORIES), required=True)
    parser.add_argument("--owner", choices=sorted(OWNERS), required=True)
    parser.add_argument("--status", choices=sorted(STATUSES), required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--counterevidence", action="append", default=[])
    parser.add_argument("--independent-article-id", action="append", default=[])
    parser.add_argument("--explicit-long-term-instruction", action="store_true")
    parser.add_argument("--author-confirmed", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--allow-repository-output",
        action="store_true",
        help="Allow repository output only after the user explicitly authorizes persistence",
    )
    args = parser.parse_args()

    event = build_event(
        article_id=args.article_id,
        summary=args.summary,
        correction=args.correction,
        category=args.category,
        owner=args.owner,
        status=args.status,
        scope=args.scope,
        evidence=args.evidence,
        counterevidence=args.counterevidence,
        independent_article_ids=args.independent_article_id,
        explicit_long_term_instruction=args.explicit_long_term_instruction,
        author_confirmed=args.author_confirmed,
    )
    output = resolve_output_path(
        args.output,
        article_id=args.article_id,
        allow_repository_output=args.allow_repository_output,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, indent=2) + "\n")
    print(f"反馈事件已生成：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
