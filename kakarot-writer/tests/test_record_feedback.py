from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "record_feedback.py"
SPEC = importlib.util.spec_from_file_location("record_feedback", MODULE_PATH)
assert SPEC and SPEC.loader
RECORDER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RECORDER
SPEC.loader.exec_module(RECORDER)


class RecordFeedbackTests(unittest.TestCase):
    def test_deterministic_error_requires_regression_test(self) -> None:
        event = RECORDER.build_event(
            article_id="article-1",
            summary="正文重复标题",
            correction="标题只进入发布参数，不进入正文",
            category="deterministic_error",
            owner="wechat-publisher",
            status="hard_rule",
            scope="公众号发布",
        )

        self.assertTrue(event["regression_test_required"])
        self.assertEqual(event["privacy"], "private_task_artifact_do_not_commit")

    def test_one_article_cannot_silently_promote_style_candidate(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot become a hard_rule"):
            RECORDER.build_event(
                article_id="article-1",
                summary="删除小标题",
                correction="少用小标题",
                category="style_candidate",
                owner="kakarot-writer",
                status="hard_rule",
                scope="所有文章",
            )

    def test_explicit_instruction_can_confirm_style_rule(self) -> None:
        event = RECORDER.build_event(
            article_id="article-1",
            summary="作者要求署名统一",
            correction="作者名固定写 kakarot",
            category="style_candidate",
            owner="kakarot-writer",
            status="hard_rule",
            scope="所有文章",
            explicit_long_term_instruction=True,
        )

        self.assertEqual(event["status"], "hard_rule")

    def test_recurrence_still_requires_author_confirmation(self) -> None:
        with self.assertRaisesRegex(ValueError, "author confirmation"):
            RECORDER.build_event(
                article_id="article-2",
                summary="两篇都删除了无证据趋势判断",
                correction="趋势判断需要证据",
                category="style_candidate",
                owner="kakarot-writer",
                status="hard_rule",
                scope="AI 解读",
                independent_article_ids=["article-1"],
            )

    def test_confirmed_recurrence_can_promote_style_rule(self) -> None:
        event = RECORDER.build_event(
            article_id="article-2",
            summary="两篇都删除了无证据趋势判断",
            correction="趋势判断需要证据",
            category="style_candidate",
            owner="kakarot-writer",
            status="hard_rule",
            scope="AI 解读",
            independent_article_ids=["article-1"],
            author_confirmed=True,
        )

        self.assertEqual(event["recurrence_count"], 2)

    def test_category_status_matrix_rejects_misclassification(self) -> None:
        for category, invalid_status in (
            ("deterministic_error", "candidate"),
            ("one_off_choice", "hard_rule"),
            ("unknown", "hard_rule"),
        ):
            with self.subTest(category=category):
                with self.assertRaises(ValueError):
                    RECORDER.build_event(
                        article_id="article-1",
                        summary="反馈原子",
                        correction="修正",
                        category=category,
                        owner="kakarot-writer",
                        status=invalid_status,
                        scope="本次测试",
                    )

    def test_repository_output_is_rejected_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            output = root / "kakarot-writer" / "feedback.json"

            with self.assertRaisesRegex(ValueError, "Git worktree"):
                RECORDER.resolve_output_path(output, article_id="article-1")

    def test_long_unredacted_evidence_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "redacted-summary"):
            RECORDER.build_event(
                article_id="article-1",
                summary="反馈",
                correction="修正",
                category="unknown",
                owner="unknown",
                status="needs_review",
                scope="未知",
                evidence=["原文" * 300],
            )

    def test_split_evidence_cannot_bypass_total_budget(self) -> None:
        with self.assertRaisesRegex(ValueError, "500-character"):
            RECORDER.build_event(
                article_id="article-1",
                summary="反馈",
                correction="修正",
                category="unknown",
                owner="unknown",
                status="needs_review",
                scope="未知",
                evidence=["x" * 300, "y" * 300],
            )

    def test_upgrade_flags_apply_only_to_style_candidates(self) -> None:
        for category, status in (
            ("deterministic_error", "hard_rule"),
            ("one_off_choice", "one_off"),
            ("unknown", "needs_review"),
        ):
            with self.subTest(category=category):
                with self.assertRaisesRegex(ValueError, "only to style_candidate"):
                    RECORDER.build_event(
                        article_id="article-1",
                        summary="反馈原子",
                        correction="修正",
                        category=category,
                        owner="kakarot-writer",
                        status=status,
                        scope="本次测试",
                        explicit_long_term_instruction=True,
                    )

    def test_default_output_paths_are_unique_for_atomic_events(self) -> None:
        paths = {
            RECORDER.resolve_output_path(None, article_id="article-1")
            for _ in range(3)
        }

        self.assertEqual(len(paths), 3)


if __name__ == "__main__":
    unittest.main()
