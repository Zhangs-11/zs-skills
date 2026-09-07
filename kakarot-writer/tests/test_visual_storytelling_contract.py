"""Check that the optional visual branch is reachable before prose generation.

These are documentation-contract checks, not model-behavior evaluations.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VisualStorytellingContractTests(unittest.TestCase):
    def test_visual_planning_precedes_prose(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertLess(
            skill.index("references/visual-storytelling.md"),
            skill.index("在可用 skills 中定位 `human-writing`"),
        )
        self.assertIn("个人叙事不强制套图解", skill)
        self.assertIn("图文分工", skill)

    def test_delivery_points_to_same_owner(self):
        delivery = (ROOT / "references/delivery.md").read_text()
        self.assertIn("(visual-storytelling.md)", delivery)
        self.assertIn("不限制承载信息的流程图", delivery)

    def test_visual_branch_has_mobile_and_factual_boundaries(self):
        text = (ROOT / "references/visual-storytelling.md").read_text()
        for requirement in (
            "360 px 和 390 px", "显示宽度", "双泳道图", "可编辑源",
            "不把所有节点再叙述一遍", "规则推演不是实测",
            "PNG", "公众号后台未验收", "不是微信官方限制",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, text)

    def test_local_reference_links_resolve(self):
        for name in ("SKILL.md", "references/delivery.md", "references/visual-storytelling.md"):
            file = ROOT / name
            for link in re.findall(r"\]\(([^)]+)\)", file.read_text()):
                if "://" not in link and not link.startswith("#"):
                    self.assertTrue((file.parent / link.split("#")[0]).exists(), link)


if __name__ == "__main__":
    unittest.main()
