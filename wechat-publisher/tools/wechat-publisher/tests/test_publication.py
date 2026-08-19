import unittest

from wechat_publisher.publication import (
    DELIVERY_APPENDIX_MARKER,
    publication_contract_findings,
    split_publication_document,
)


class PublicationContractTests(unittest.TestCase):
    def test_frontmatter_and_delivery_appendix_never_enter_public_body(self) -> None:
        md = """---
title: 测试文章
author: kakarot
---

第一段正文。

<!-- kakarot:delivery-appendix -->

## 截图清单

- 内部截图
"""

        document = split_publication_document(md)

        self.assertTrue(document.had_frontmatter)
        self.assertEqual(document.public_markdown, "第一段正文。\n")
        self.assertIn("截图清单", document.delivery_appendix)
        self.assertNotIn("title:", document.public_markdown)

    def test_author_and_contact_footer_remain_in_public_body(self) -> None:
        md = """正文最后一段。

> / 作者：kakarot
> / 投稿、合作或交流，欢迎在公众号后台留言

<!-- kakarot:delivery-appendix -->

## 截图清单

- 内部截图
"""

        document = split_publication_document(md)

        self.assertIn("> / 作者：kakarot", document.public_markdown)
        self.assertIn("投稿、合作或交流", document.public_markdown)
        self.assertNotIn("截图清单", document.public_markdown)

    def test_repeated_title_is_a_hard_preflight_error(self) -> None:
        findings = publication_contract_findings(
            title="晚上 11 点下班，我为什么还有精力继续学习？",
            md="# 《晚上11点下班，我为什么还有精力继续学习？》\n\n正文",
        )

        self.assertTrue(any("重复" in finding for finding in findings))

    def test_leading_horizontal_rule_is_not_mistaken_for_frontmatter(self) -> None:
        md = "---\n\n开场正文。\n\n---\n\n后续正文。"

        document = split_publication_document(md)

        self.assertFalse(document.had_frontmatter)
        self.assertTrue(document.public_markdown.startswith("---"))

    def test_internal_headings_require_explicit_appendix_marker(self) -> None:
        findings = publication_contract_findings(
            title="文章标题",
            md="正文\n\n## 截图清单\n\n- 一张图",
        )

        self.assertTrue(any(DELIVERY_APPENDIX_MARKER in finding for finding in findings))

    def test_heading_like_text_inside_code_block_is_allowed(self) -> None:
        findings = publication_contract_findings(
            title="文章标题",
            md="正文\n\n```markdown\n# 示例标题\n## 截图清单\n```",
        )

        self.assertEqual(findings, [])

    def test_inline_marker_text_does_not_truncate_public_body(self) -> None:
        md = "正文解释 `<!-- kakarot:delivery-appendix -->` 的含义。\n\n第二段仍是正文。"

        document = split_publication_document(md)

        self.assertIn("第二段仍是正文", document.public_markdown)
        self.assertEqual(document.delivery_appendix, "")

    def test_marker_inside_code_block_does_not_truncate_public_body(self) -> None:
        md = "前文\n\n```markdown\n<!-- kakarot:delivery-appendix -->\n```\n\n后文"

        document = split_publication_document(md)

        self.assertIn("后文", document.public_markdown)
        self.assertEqual(document.delivery_appendix, "")

    def test_marker_inside_quote_does_not_truncate_public_body(self) -> None:
        md = "前文\n\n> <!-- kakarot:delivery-appendix -->\n> 这是引用内容\n\n后文"

        document = split_publication_document(md)

        self.assertIn("后文", document.public_markdown)
        self.assertEqual(document.delivery_appendix, "")

    def test_setext_and_html_h1_are_rejected(self) -> None:
        for md in (
            "开场\n\n文章标题\n========\n\n正文",
            "开场\n\n<h1>文章标题</h1>\n\n正文",
        ):
            with self.subTest(md=md):
                findings = publication_contract_findings(title="文章标题", md=md)
                self.assertTrue(any("重复" in item for item in findings))

    def test_inline_html_h1_is_rejected(self) -> None:
        findings = publication_contract_findings(
            title="文章标题",
            md="开场 <h1>文章标题</h1> 结束\n\n正文",
        )

        self.assertTrue(any("重复" in item for item in findings))

    def test_quoted_non_ascii_yaml_key_is_removed(self) -> None:
        md = '---\n"标题": 测试\n---\n\n正文'

        document = split_publication_document(md)

        self.assertTrue(document.had_frontmatter)
        self.assertEqual(document.public_markdown, "正文\n")

    def test_internal_heading_suffix_is_still_rejected(self) -> None:
        findings = publication_contract_findings(
            title="文章标题",
            md="正文\n\n## 截图清单（内部）\n\n- 一张图",
        )

        self.assertTrue(any("截图清单" in item for item in findings))

    def test_public_sources_heading_is_allowed(self) -> None:
        findings = publication_contract_findings(
            title="文章标题",
            md="正文\n\n## 关键来源\n\n- [官方文档](https://example.com)",
        )

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
