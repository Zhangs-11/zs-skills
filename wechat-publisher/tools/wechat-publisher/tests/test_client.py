import unittest

from wechat_publisher.client import WeChatClient
from wechat_publisher.config import Settings


class RecordingClient(WeChatClient):
    def __init__(self) -> None:
        settings = Settings(
            wechat_app_id="wx-test",
            wechat_app_secret="secret",
            wechat_author="Kakarot",
            wechat_default_cover_media_id="cover-media",
        )
        super().__init__(settings)
        self.calls = []

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        self.calls.append((method, path, kwargs))
        return {"media_id": "draft-media"}


class ClientPayloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_update_draft_sends_single_article_payload(self) -> None:
        client = RecordingClient()

        await client.update_draft(
            "draft-media",
            "Title",
            "<p>body</p>",
            digest="A compact summary",
            content_source_url="https://example.com/source",
            show_cover_pic=1,
        )

        method, path, kwargs = client.calls[0]
        payload = kwargs["json"]
        self.assertEqual(method, "POST")
        self.assertEqual(path, "/draft/update")
        self.assertEqual(payload["media_id"], "draft-media")
        self.assertEqual(payload["index"], 0)
        self.assertIsInstance(payload["articles"], dict)
        self.assertEqual(payload["articles"]["thumb_media_id"], "cover-media")
        self.assertEqual(payload["articles"]["digest"], "A compact summary")
        self.assertEqual(payload["articles"]["content_source_url"], "https://example.com/source")
        self.assertEqual(payload["articles"]["show_cover_pic"], 1)

    async def test_create_draft_requires_cover_media_id(self) -> None:
        settings = Settings(
            wechat_app_id="wx-test",
            wechat_app_secret="secret",
            wechat_author="Kakarot",
            wechat_default_cover_media_id="",
        )
        client = WeChatClient(settings)

        with self.assertRaisesRegex(ValueError, "cover media_id"):
            await client.create_draft("Title", "<p>body</p>")


if __name__ == "__main__":
    unittest.main()
