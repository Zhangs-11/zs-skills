import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from wechat_publisher.cli import _derive_digest, _dispatch, _preflight_findings
from wechat_publisher.image import AssetProcessingError


class CliHelperTests(unittest.TestCase):
    def test_derive_digest_uses_first_meaningful_paragraph(self) -> None:
        md = "# 标题\n\n![图](x.png)\n\n**DeepSeek 的关键变化**，不是便宜，而是把推理模型的使用门槛打下来。后面继续。"

        digest = _derive_digest(md)

        self.assertEqual(
            digest,
            "DeepSeek 的关键变化，不是便宜，而是把推理模型的使用门槛打下来。后面继续。",
        )

    def test_preflight_reports_placeholders_missing_images_and_cover(self) -> None:
        md = "正文\n\n[插图：架构图]\n\n![本地图](missing.png)"

        findings = _preflight_findings(
            title="",
            md=md,
            base_dir=None,
            cover_file=None,
            cover_media_id=None,
        )

        self.assertTrue(any("标题" in finding for finding in findings))
        self.assertTrue(any("占位符" in finding for finding in findings))
        self.assertTrue(any("图片" in finding for finding in findings))
        self.assertFalse(any("封面" in finding for finding in findings))

    def test_preflight_accepts_ready_local_article(self) -> None:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            (base_dir / "body.png").write_bytes(b"png")
            (base_dir / "cover.png").write_bytes(b"png")

            findings = _preflight_findings(
                title="文章标题",
                md="正文\n\n![配图](body.png)",
                base_dir=base_dir,
                cover_file=str(base_dir / "cover.png"),
                cover_media_id=None,
            )

        self.assertEqual(findings, [])

    def test_preflight_rejects_directory_used_as_image(self) -> None:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            (base_dir / "images").mkdir()
            findings = _preflight_findings(
                title="文章标题",
                md="正文\n\n![配图](images)",
                base_dir=base_dir,
                cover_file=None,
                cover_media_id="existing-cover",
            )

        self.assertTrue(any("图片文件不存在" in item for item in findings))


class CliCoverFileTests(unittest.IsolatedAsyncioTestCase):
    async def test_cover_file_is_uploaded_before_create(self) -> None:
        client = FakeClient()
        args = SimpleNamespace(
            command="create",
            title="标题",
            content_file=None,
            stdin=True,
            cover_file=__file__,
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

        self.assertEqual(client.uploaded_cover, __file__)
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
            patch(
                "wechat_publisher.cli.prepare_markdown_assets",
                new_callable=AsyncMock,
            ) as prepare_assets,
        ):
            with self.assertRaisesRegex(ValueError, "Choose either"):
                await _dispatch(args)

        prepare_assets.assert_not_awaited()

    async def test_unresolved_placeholder_does_not_upload_cover(self) -> None:
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
            patch(
                "wechat_publisher.cli._read_content",
                return_value=("正文\n\n[插图：未完成]", None),
            ),
        ):
            with self.assertRaisesRegex(AssetProcessingError, "未解析"):
                await _dispatch(args)

        self.assertIsNone(client.uploaded_cover)


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
