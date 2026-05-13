import asyncio

import httpx

from .config import Settings
from .models import (
    Article,
    CreateDraftRequest,
    CreateDraftResponse,
    UpdateDraftRequest,
    UpdateDraftResponse,
    UploadImageResponse,
)
from .token import TokenManager

API_BASE = "https://api.weixin.qq.com/cgi-bin"


class WeChatClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.token_mgr = TokenManager(settings)

    async def _ensure_token(self) -> str:
        cached = self.token_mgr.get_cached()
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{API_BASE}/token",
                params={
                    "grant_type": "client_credential",
                    "appid": self.settings.wechat_app_id,
                    "secret": self.settings.wechat_app_secret,
                },
            )
            body = r.json()
            if "access_token" not in body:
                raise RuntimeError(f"token fetch failed: {body}")
            self.token_mgr.save(body["access_token"], body["expires_in"])
            return body["access_token"]

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        last_err: Exception | None = None
        for attempt in range(3):
            token = await self._ensure_token()
            url = f"{API_BASE}{path}?access_token={token}"
            async with httpx.AsyncClient(timeout=30) as client:
                try:
                    r = await client.request(method, url, **kwargs)
                    data = r.json()
                except httpx.TimeoutException:
                    last_err = Exception("timeout")
                    await asyncio.sleep(1)
                    continue

                code = data.get("errcode", 0)
                if code == 40001:
                    self.token_mgr.invalidate()
                    continue
                if code == 45009:
                    wait = [1, 4, 10][min(attempt, 2)]
                    await asyncio.sleep(wait)
                    continue
                if code != 0:
                    raise RuntimeError(
                        f"WeChat API error ({code}): {data.get('errmsg', '')}"
                    )
                return data
        raise last_err or RuntimeError("request failed after retries")

    async def create_draft(self, title: str, content_html: str) -> CreateDraftResponse:
        article = Article(
            title=title,
            author=self.settings.wechat_author,
            content=content_html,
        )
        if self.settings.wechat_default_cover_media_id:
            article.thumb_media_id = self.settings.wechat_default_cover_media_id
        req = CreateDraftRequest(articles=[article])
        data = await self._request(
            "POST", "/draft/add", json=req.model_dump(exclude_none=True)
        )
        return CreateDraftResponse(media_id=data.get("media_id", ""))

    async def update_draft(
        self, media_id: str, title: str, content_html: str
    ) -> UpdateDraftResponse:
        article = Article(
            title=title,
            author=self.settings.wechat_author,
            content=content_html,
        )
        if self.settings.wechat_default_cover_media_id:
            article.thumb_media_id = self.settings.wechat_default_cover_media_id
        req = UpdateDraftRequest(
            media_id=media_id,
            articles=[article],
        )
        data = await self._request(
            "POST", "/draft/update", json=req.model_dump(exclude_none=True)
        )
        return UpdateDraftResponse(media_id=data.get("media_id", ""))

    async def upload_image(self, file_path: str) -> UploadImageResponse:
        token = await self._ensure_token()
        async with httpx.AsyncClient(timeout=60) as client:
            with open(file_path, "rb") as f:
                r = await client.post(
                    f"{API_BASE}/media/uploadimg",
                    params={"access_token": token},
                    files={"media": f},
                )
            data = r.json()
            if "url" not in data:
                raise RuntimeError(f"image upload failed: {data}")
            return UploadImageResponse(url=data["url"])

    async def upload_cover(self, file_path: str) -> str:
        """Upload a permanent image material and return its media_id (for cover)."""
        token = await self._ensure_token()
        async with httpx.AsyncClient(timeout=60) as client:
            with open(file_path, "rb") as f:
                r = await client.post(
                    f"{API_BASE}/material/add_material",
                    params={"access_token": token, "type": "image"},
                    files={"media": f},
                )
            data = r.json()
            if "media_id" not in data:
                raise RuntimeError(f"cover upload failed: {data}")
            return data["media_id"]
