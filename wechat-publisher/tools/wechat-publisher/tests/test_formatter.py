import unittest

from bs4 import BeautifulSoup

from wechat_publisher.formatter import markdown_to_wechat_html


class FormatterTests(unittest.TestCase):
    def test_first_sentence_is_not_automatically_bolded(self) -> None:
        html = markdown_to_wechat_html("DeepSeek真正重要的变化，是把推理模型的使用门槛打下来。这里是第二句，应该保持普通正文。")

        self.assertNotIn("font-size: 17px; font-weight: 700", html)

    def test_external_links_are_moved_to_reference_section(self) -> None:
        html = markdown_to_wechat_html("参考 [OpenAI](https://openai.com) 的发布。")
        text = BeautifulSoup(html, "html.parser").get_text(" ")

        self.assertIn("参考", text)
        self.assertIn("OpenAI", text)
        self.assertIn("参考资料", html)
        self.assertIn("[1] OpenAI：https://openai.com", html)
        self.assertNotIn("<a ", html)

    def test_tables_render_as_table_html(self) -> None:
        html = markdown_to_wechat_html("| 模型 | 价格 |\n|---|---|\n| A | 低 |")

        self.assertIn("<table", html)
        self.assertIn("<th", html)
        self.assertIn("<td", html)


if __name__ == "__main__":
    unittest.main()
