import unittest

from wechat_publisher.cli import _derive_digest


class CliHelperTests(unittest.TestCase):
    def test_derive_digest_uses_first_meaningful_paragraph(self) -> None:
        md = "# 标题\n\n![图](x.png)\n\n**DeepSeek 的关键变化**，不是便宜，而是把推理模型的使用门槛打下来。后面继续。"

        digest = _derive_digest(md)

        self.assertEqual(
            digest,
            "DeepSeek 的关键变化，不是便宜，而是把推理模型的使用门槛打下来。后面继续。",
        )


if __name__ == "__main__":
    unittest.main()
