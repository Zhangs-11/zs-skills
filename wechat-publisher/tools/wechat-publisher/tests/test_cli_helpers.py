import unittest
from types import SimpleNamespace
from unittest.mock import patch

from wechat_publisher.cli import _derive_digest, _dispatch


class CliHelperTests(unittest.TestCase):
    def test_derive_digest_uses_first_meaningful_paragraph(self) -> None:
        md = "# 标题\n\n![图](x.png)\n\n**DeepSeek 的关键变化**，不是便宜，而是把推理模型的使用门槛打下来。后面继续。"

        digest = _derive_digest(md)

        self.assertEqual(
            digest,
            "DeepSeek 的关键变化，不是便宜，而是把推理模型的使用门槛打下来。后面继续。",
        )


class CliCoverFileTests(unittest.IsolatedAsyncioTestCase):
    async def test_cover_file_is_uploaded_before_create(self) -> None:
        client = FakeClient()
        args = SimpleNamespace(
            command="create",
            title="标题",
            content_file=None,
            stdin=True,
            cover_file="cover.png",
            cover_media_id=None,
            digest="摘要",
            source_url=None,
            show_cover_pic=False,
        )

        with (
            patch("wechat_publisher.cli.Settings", return_value=object()),
            patch("wechat_publisher.cli.WeChatClient", return_value=client),
            patch("wechat_publisher.cli._read_content", return_value=("正文", None)),
            patch("wechat_publisher.cli.prepare_markdown_assets", return_value="正文"),
            patch("wechat_publisher.cli.markdown_to_wechat_html", return_value="<p>正文</p>"),
        ):
            await _dispatch(args)

        self.assertEqual(client.uploaded_cover, "cover.png")
        self.assertEqual(client.created["cover_media_id"], "uploaded-cover-media")

    async def test_cover_file_cannot_be_combined_with_cover_media_id(self) -> None:
        client = FakeClient()
        args = SimpleNamespace(
            command="create",
            title="标题",
            content_file=None,
            stdin=True,
            cover_file="cover.png",
            cover_media_id="existing-cover",
            digest="摘要",
            source_url=None,
            show_cover_pic=False,
        )

        with (
            patch("wechat_publisher.cli.Settings", return_value=object()),
            patch("wechat_publisher.cli.WeChatClient", return_value=client),
        ):
            with self.assertRaisesRegex(ValueError, "Choose either"):
                await _dispatch(args)


class FakeClient:
    def __init__(self) -> None:
        self.uploaded_cover = None
        self.created = None

    async def upload_cover(self, file_path: str) -> str:
        self.uploaded_cover = file_path
        return "uploaded-cover-media"

    async def create_draft(self, title: str, html: str, **kwargs):
        self.created = kwargs
        return SimpleNamespace(media_id="draft-media")


if __name__ == "__main__":
    unittest.main()
