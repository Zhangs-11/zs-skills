from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "analyze_revision.py"
SPEC = importlib.util.spec_from_file_location("analyze_revision", MODULE_PATH)
assert SPEC and SPEC.loader
ANALYZER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ANALYZER
SPEC.loader.exec_module(ANALYZER)


class AnalyzeRevisionTests(unittest.TestCase):
    def test_report_keeps_observation_separate_from_preference(self) -> None:
        draft = "# 标题\n\n先说结论：这不是效率问题，而是判断问题。\n\n趋势会改变一切。"
        final = "# 标题\n\n我后来发现，自己缺的是判断依据。"
        report = ANALYZER.build_report(draft, final, Path("draft.md"), Path("final.md"))

        self.assertLess(report["metrics"]["delta"]["characters"], 0)
        self.assertTrue(report["changed_blocks"])
        self.assertIn("不自动证明作者偏好", report["interpretation_boundary"])
        self.assertNotIn("作者喜欢", str(report))


if __name__ == "__main__":
    unittest.main()
