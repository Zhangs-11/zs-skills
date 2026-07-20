import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from wechat_publisher.client import WeChatClient, _parse_json_response
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
        if path == "/draft/get":
            return {"news_item": [{"thumb_media_id": "existing-cover"}]}
        if path == "/draft/update":
            return {"errcode": 0, "errmsg": "ok"}
        return {"media_id": "draft-media"}


class ClientPayloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_http_status_error_does_not_expose_query_secrets(self) -> None:
        response = httpx.Response(
            500,
            request=httpx.Request(
                "GET",
                "https://api.weixin.qq.com/cgi-bin/token?secret=TOPSECRET&access_token=TOKEN",
            ),
        )

        with self.assertRaises(RuntimeError) as caught:
            _parse_json_response(response)

        message = str(caught.exception)
        self.assertNotIn("TOPSECRET", message)
        self.assertNotIn("TOKEN", message)
        self.assertEqual(message, "WeChat API returned HTTP 500")

    async def test_update_draft_sends_single_article_payload(self) -> None:
        client = RecordingClient()

        result = await client.update_draft(
            "draft-media",
            "Title",
            "<p>body</p>",
            digest="A compact summary",
            content_source_url="https://example.com/source",
            show_cover_pic=1,
        )

        self.assertEqual(client.calls[0][1], "/draft/get")
        method, path, kwargs = client.calls[1]
        payload = kwargs["json"]
        self.assertEqual(method, "POST")
        self.assertEqual(path, "/draft/update")
        self.assertEqual(payload["media_id"], "draft-media")
        self.assertEqual(payload["index"], 0)
        self.assertIsInstance(payload["articles"], dict)
        self.assertEqual(payload["articles"]["thumb_media_id"], "existing-cover")
        self.assertEqual(payload["articles"]["digest"], "A compact summary")
        self.assertEqual(payload["articles"]["content_source_url"], "https://example.com/source")
        self.assertEqual(payload["articles"]["show_cover_pic"], 1)
        self.assertEqual(result.media_id, "draft-media")

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

    async def test_create_draft_rejects_success_response_without_media_id(self) -> None:
        client = RecordingClient()
        client._request = AsyncMock(return_value={})

        with self.assertRaisesRegex(RuntimeError, "media_id"):
            await client.create_draft("Title", "<p>body</p>")

    async def test_draft_read_timeout_is_not_retried(self) -> None:
        client = WeChatClient(RecordingClient().settings)
        client._ensure_token = AsyncMock(return_value="token")
        http = AsyncMock()
        http.request.side_effect = httpx.ReadTimeout("response timed out")
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=http)
        context.__aexit__ = AsyncMock(return_value=None)

        with patch("wechat_publisher.client.httpx.AsyncClient", return_value=context):
            with self.assertRaisesRegex(RuntimeError, "outcome is unknown"):
                await client._request("POST", "/draft/add", json={"articles": []})

        http.request.assert_awaited_once()

    async def test_draft_write_timeout_is_not_retried(self) -> None:
        client = WeChatClient(RecordingClient().settings)
        client._ensure_token = AsyncMock(return_value="token")
        http = AsyncMock()
        http.request.side_effect = httpx.WriteTimeout("request body timed out")
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=http)
        context.__aexit__ = AsyncMock(return_value=None)

        with patch("wechat_publisher.client.httpx.AsyncClient", return_value=context):
            with self.assertRaisesRegex(RuntimeError, "outcome is unknown"):
                await client._request("POST", "/draft/add", json={"articles": []})

        http.request.assert_awaited_once()

    async def test_upload_image_refreshes_expired_token_once(self) -> None:
        client = RecordingClient()
        client._ensure_token = AsyncMock(side_effect=["expired", "fresh"])
        client.token_mgr.invalidate = MagicMock()
        expired = httpx.Response(
            200,
            json={"errcode": 40001, "errmsg": "invalid credential"},
            request=httpx.Request("POST", "https://api.weixin.qq.com/upload"),
        )
        success = httpx.Response(
            200,
            json={"url": "https://mmbiz.qpic.cn/uploaded"},
            request=httpx.Request("POST", "https://api.weixin.qq.com/upload"),
        )
        http = AsyncMock()
        http.post.side_effect = [expired, success]
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=http)
        context.__aexit__ = AsyncMock(return_value=None)

        with patch("wechat_publisher.client.httpx.AsyncClient", return_value=context):
            result = await client.upload_image(__file__)

        self.assertEqual(result.url, "https://mmbiz.qpic.cn/uploaded")
        self.assertEqual(http.post.await_count, 2)
        client.token_mgr.invalidate.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
