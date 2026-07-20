import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from wechat_publisher.image import AssetProcessingError, prepare_markdown_assets
import wechat_publisher.image as image_module


class FakeUploadResult:
    def __init__(self, url: str) -> None:
        self.url = url


class FakeClient:
    def __init__(self) -> None:
        self.uploaded = []

    async def upload_image(self, file_path: str) -> FakeUploadResult:
        self.uploaded.append(file_path)
        return FakeUploadResult("https://mmbiz.qpic.cn/local-image")


class AssetProcessingTests(unittest.IsolatedAsyncioTestCase):
    async def test_unresolved_image_placeholder_blocks_publish(self) -> None:
        md = "正文\n\n[插图：传统RAG工作流]\n[绘图提示：clean technical diagram]"

        with self.assertRaisesRegex(AssetProcessingError, "未解析插图占位符"):
            await prepare_markdown_assets(md, FakeClient())

    async def test_local_markdown_image_is_uploaded_and_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "cover.png"
            image_path.write_bytes(b"png")
            md = "![流程图](cover.png)"
            client = FakeClient()

            result = await prepare_markdown_assets(md, client, base_dir=Path(tmp))

        self.assertEqual(result, "![流程图](https://mmbiz.qpic.cn/local-image)")
        self.assertEqual(len(client.uploaded), 1)

    async def test_existing_wechat_cdn_image_is_left_unchanged(self) -> None:
        md = "![图](https://mmbiz.qpic.cn/example)"

        result = await prepare_markdown_assets(md, FakeClient())

        self.assertEqual(result, md)

    def test_private_remote_image_addresses_are_rejected(self) -> None:
        for url in (
            "http://127.0.0.1/image.png",
            "http://169.254.169.254/latest/meta-data",
            "http://[::1]/image.png",
        ):
            with self.subTest(url=url):
                with self.assertRaisesRegex(AssetProcessingError, "private or local"):
                    image_module._validate_remote_image_url(url)

    def test_remote_response_requires_supported_image_content_type(self) -> None:
        with self.assertRaisesRegex(AssetProcessingError, "content type"):
            image_module._validate_remote_image_response(
                "text/html",
                content_length=120,
            )

    def test_remote_response_rejects_declared_oversize_body(self) -> None:
        with self.assertRaisesRegex(AssetProcessingError, "too large"):
            image_module._validate_remote_image_response(
                "image/png",
                content_length=image_module.MAX_REMOTE_IMAGE_BYTES + 1,
            )

    async def test_streaming_failure_removes_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(
                image_module,
                "download_public_url",
                side_effect=image_module.SecureDownloadError("remote image is too large"),
            ):
                with self.assertRaisesRegex(AssetProcessingError, "too large"):
                    await image_module.upload_image_from_url(
                        FakeClient(),
                        "https://example.com/image.png",
                    )

            self.assertEqual(list(Path(tmp).iterdir()), [])

    async def test_redirect_is_rejected_before_upload(self) -> None:
        client = FakeClient()

        with patch.object(
            image_module,
            "download_public_url",
            side_effect=image_module.SecureDownloadError(
                "remote image redirects are not allowed"
            ),
        ):
            with self.assertRaisesRegex(AssetProcessingError, "redirects"):
                await image_module.upload_image_from_url(
                    client,
                    "https://example.com/image.png",
                )

        self.assertEqual(client.uploaded, [])


if __name__ == "__main__":
    unittest.main()
