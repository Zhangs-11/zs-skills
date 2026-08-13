import unittest
from unittest.mock import patch

from wechat_publisher.linkcheck import check_external_links, extract_external_links


class ExtractExternalLinksTests(unittest.TestCase):
    def test_extracts_markdown_and_bare_links_without_duplicates(self) -> None:
        md = "[官方文档](https://github.com/org/repo/blob/master/README.md)\n\nhttps://example.com/docs。"

        self.assertEqual(
            extract_external_links(md),
            [
                "https://example.com/docs",
                "https://github.com/org/repo/blob/master/README.md",
            ],
        )

    def test_ignores_links_in_code_and_comments_and_keeps_balanced_parentheses(self) -> None:
        md = """```text
https://example.com/in-code
```
<!-- https://example.com/in-comment -->
[函数](https://en.wikipedia.org/wiki/Function_(mathematics))
"""

        self.assertEqual(
            extract_external_links(md),
            ["https://en.wikipedia.org/wiki/Function_(mathematics)"],
        )

    def test_accepts_uppercase_scheme(self) -> None:
        self.assertEqual(
            extract_external_links("[文档](HTTPS://example.com/docs)"),
            ["HTTPS://example.com/docs"],
        )

    def test_extracts_rendered_html_links(self) -> None:
        md = '正文 <a href="https://example.com/inline">文档</a>\n\n<div><a href="https://example.com/block">资料</a></div>'

        self.assertEqual(
            extract_external_links(md),
            ["https://example.com/block", "https://example.com/inline"],
        )

    def test_bare_url_stops_before_chinese_punctuation_and_prose(self) -> None:
        md = "链接是 https://example.com/docs，这里继续。"

        self.assertEqual(extract_external_links(md), ["https://example.com/docs"])


class CheckExternalLinksTests(unittest.IsolatedAsyncioTestCase):
    async def test_reports_a_404_link(self) -> None:
        with patch("wechat_publisher.linkcheck.check_public_url_status", return_value=404):
            findings = await check_external_links(
                "[错误链接](https://github.com/org/repo/blob/main/missing.md)"
            )

        self.assertEqual(len(findings), 1)
        self.assertIn("HTTP 404", findings[0])

    async def test_accepts_reachable_link(self) -> None:
        with patch("wechat_publisher.linkcheck.check_public_url_status", return_value=200):
            findings = await check_external_links("[文档](https://example.com/docs)")

        self.assertEqual(findings, [])

    async def test_private_link_is_rejected_without_a_request(self) -> None:
        findings = await check_external_links("[内部](http://127.0.0.1/delete?id=1)")

        self.assertEqual(len(findings), 1)
        self.assertIn("无法安全验证", findings[0])


if __name__ == "__main__":
    unittest.main()
