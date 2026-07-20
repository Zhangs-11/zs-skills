import asyncio
from typing import Any

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


class WeChatAPIError(RuntimeError):
    def __init__(self, code: int, message: str, payload: dict[str, Any]) -> None:
        super().__init__(f"WeChat API error ({code}): {message}")
        self.code = code
        self.message = message
        self.payload = payload


class WeChatClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.token_mgr = TokenManager(settings)

    async def _ensure_token(self) -> str:
        cached = self.token_mgr.get_cached()
        if cached:
            return cached

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(
                f"{API_BASE}/token",
                params={
                    "grant_type": "client_credential",
                    "appid": self.settings.wechat_app_id,
                    "secret": self.settings.wechat_app_secret,
                },
            )
            if r.is_error:
                raise RuntimeError(f"token fetch returned HTTP {r.status_code}")
            body = _parse_json_response(r)
            if "access_token" not in body:
                raise RuntimeError(f"token fetch failed: {body}")
            self.token_mgr.save(body["access_token"], body["expires_in"])
            return body["access_token"]

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        last_err: Exception | None = None
        is_draft_mutation = method.upper() == "POST" and path in {
            "/draft/add",
            "/draft/update",
        }
        for attempt in range(3):
            token = await self._ensure_token()
            url = f"{API_BASE}{path}?access_token={token}"
            async with httpx.AsyncClient(timeout=30) as client:
                try:
                    r = await client.request(method, url, **kwargs)
                    if r.is_error:
                        if is_draft_mutation:
                            raise RuntimeError(
                                "WeChat draft request returned an HTTP failure after it may "
                                "have been processed; the outcome is unknown. Inspect the "
                                "draft box before retrying."
                            )
                        last_err = RuntimeError(
                            f"WeChat API returned HTTP {r.status_code}"
                        )
                        await asyncio.sleep(1)
                        continue
                    data = _parse_json_response(r)
                except httpx.TransportError as exc:
                    if is_draft_mutation:
                        raise RuntimeError(
                            "WeChat draft request failed after it may have been sent; "
                            "the outcome is unknown. Inspect the draft box before retrying."
                        ) from exc
                    last_err = RuntimeError("request transport failed")
                    await asyncio.sleep(1)
                    continue
                except httpx.HTTPError as exc:
                    if is_draft_mutation:
                        raise RuntimeError(
                            "WeChat draft request returned an HTTP failure after it may have "
                            "been processed; the outcome is unknown. Inspect the draft box "
                            "before retrying."
                        ) from exc
                    last_err = RuntimeError("HTTP request failed")
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
                    raise WeChatAPIError(code, data.get("errmsg", ""), data)
                return data
        raise last_err or RuntimeError("request failed after retries")

    async def create_draft(
        self,
        title: str,
        content_html: str,
        *,
        cover_media_id: str | None = None,
        digest: str | None = None,
        content_source_url: str | None = None,
        show_cover_pic: int = 0,
    ) -> CreateDraftResponse:
        article = self._build_article(
            title=title,
            content_html=content_html,
            cover_media_id=cover_media_id,
            digest=digest,
            content_source_url=content_source_url,
            show_cover_pic=show_cover_pic,
        )
        req = CreateDraftRequest(articles=[article])
        data = await self._request(
            "POST", "/draft/add", json=req.model_dump(exclude_none=True)
        )
        media_id = data.get("media_id")
        if not isinstance(media_id, str) or not media_id:
            raise RuntimeError(f"draft creation response missing media_id: {data}")
        return CreateDraftResponse(media_id=media_id)

    async def get_draft_cover(self, media_id: str) -> str | None:
        """Fetch the existing draft's thumb_media_id."""
        data = await self._request(
            "POST", "/draft/get", json={"media_id": media_id}
        )
        items = data.get("news_item") or []
        if items:
            return items[0].get("thumb_media_id")
        return None

    async def update_draft(
        self,
        media_id: str,
        title: str,
        content_html: str,
        *,
        cover_media_id: str | None = None,
        digest: str | None = None,
        content_source_url: str | None = None,
        show_cover_pic: int = 0,
    ) -> UpdateDraftResponse:
        if not cover_media_id:
            cover_media_id = await self.get_draft_cover(media_id)
        article = self._build_article(
            title=title,
            content_html=content_html,
            cover_media_id=cover_media_id,
            digest=digest,
            content_source_url=content_source_url,
            show_cover_pic=show_cover_pic,
        )
        req = UpdateDraftRequest(
            media_id=media_id,
            articles=article,
        )
        await self._request(
            "POST", "/draft/update", json=req.model_dump(exclude_none=True)
        )
        # 微信 draft/update 的成功响应通常只有 errcode/errmsg，不返回 media_id。
        # 更新后的草稿仍使用调用方传入的 media_id。
        return UpdateDraftResponse(media_id=media_id)

    def _build_article(
        self,
        *,
        title: str,
        content_html: str,
        cover_media_id: str | None,
        digest: str | None,
        content_source_url: str | None,
        show_cover_pic: int,
    ) -> Article:
        resolved_cover = cover_media_id or self.settings.wechat_default_cover_media_id
        if not resolved_cover:
            raise ValueError(
                "cover media_id is required. Set WECHAT_DEFAULT_COVER_MEDIA_ID "
                "or pass --cover-media-id."
            )

        return Article(
            title=title,
            author=self.settings.wechat_author,
            content=content_html,
            thumb_media_id=resolved_cover,
            digest=digest,
            content_source_url=content_source_url,
            show_cover_pic=show_cover_pic,
        )

    async def upload_image(self, file_path: str) -> UploadImageResponse:
        url = await self._upload_file(
            "/media/uploadimg",
            file_path,
            response_key="url",
            params={},
            failure_label="image upload",
        )
        return UploadImageResponse(url=url)

    async def upload_cover(self, file_path: str) -> str:
        """Upload a permanent image material and return its media_id (for cover)."""
        return await self._upload_file(
            "/material/add_material",
            file_path,
            response_key="media_id",
            params={"type": "image"},
            failure_label="cover upload",
        )

    async def _upload_file(
        self,
        path: str,
        file_path: str,
        *,
        response_key: str,
        params: dict[str, str],
        failure_label: str,
    ) -> str:
        for attempt in range(2):
            token = await self._ensure_token()
            request_params = {"access_token": token, **params}
            async with httpx.AsyncClient(timeout=60) as client:
                with open(file_path, "rb") as f:
                    response = await client.post(
                        f"{API_BASE}{path}",
                        params=request_params,
                        files={"media": f},
                    )
            data = _parse_json_response(response)
            code = data.get("errcode", 0)
            if code == 40001 and attempt == 0:
                self.token_mgr.invalidate()
                continue
            if code != 0:
                raise WeChatAPIError(code, data.get("errmsg", ""), data)
            value = data.get(response_key)
            if not isinstance(value, str) or not value:
                raise RuntimeError(f"{failure_label} failed: {data}")
            return value
        raise RuntimeError(f"{failure_label} failed after token refresh")


def _parse_json_response(response: httpx.Response) -> dict[str, Any]:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"WeChat API returned HTTP {exc.response.status_code}"
        ) from None
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("WeChat API returned a non-JSON response") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"WeChat API returned unexpected JSON: {data!r}")
    return data
