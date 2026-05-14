import tempfile
import unittest
from pathlib import Path

from wechat_publisher.image import AssetProcessingError, prepare_markdown_assets


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


if __name__ == "__main__":
    unittest.main()
