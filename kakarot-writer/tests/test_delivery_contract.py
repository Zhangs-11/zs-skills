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


if __name__ == "__main__":
    unittest.main()
