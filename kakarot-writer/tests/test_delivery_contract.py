import unittest
from pathlib import Path


class DeliveryContractTests(unittest.TestCase):
    def test_public_footer_contains_author_and_contact_entry(self) -> None:
        delivery = (
            Path(__file__).resolve().parents[1] / "references" / "delivery.md"
        ).read_text(encoding="utf-8")

        footer = (
            "> / 作者：kakarot\n"
            "> / 投稿、合作或交流，欢迎在公众号后台留言"
        )
        self.assertIn(footer, delivery)
        self.assertNotIn("投稿或爆料", delivery)

    def test_emphasis_preserves_text_and_is_conditional(self) -> None:
        delivery = (
            Path(__file__).resolve().parents[1] / "references" / "delivery.md"
        ).read_text(encoding="utf-8")
        for requirement in (
            "可选择复制的原生文字", "具体元素的行内 style",
            "颜色不能成为唯一", "没有重点材料的文章不增加区块",
            "去样式检查", "未进后台只报告本地预览结果",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, delivery)

    def test_delivery_links_require_actual_access_verification(self) -> None:
        delivery = (
            Path(__file__).resolve().parents[1] / "references" / "delivery.md"
        ).read_text(encoding="utf-8")
        for requirement in (
            "逐个验证最终发给用户的链接", "状态及响应内容",
            "引用图片是否加载", "无法验证用户端访问时明确说明限制",
            "依赖服务持续运行", "不能靠关闭安全边界",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, delivery)


if __name__ == "__main__":
    unittest.main()
