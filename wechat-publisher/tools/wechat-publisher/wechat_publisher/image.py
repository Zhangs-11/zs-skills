import tempfile
from pathlib import Path

import httpx

from .client import WeChatClient
from .config import Settings


async def upload_image_from_url(client: WeChatClient, url: str) -> str:
    """Download image from *url*, upload to WeChat CDN, return WeChat URL."""
    async with httpx.AsyncClient(timeout=30) http:
        r = await http.get(url)
        r.raise_for_status()

    ext = _guess_ext(r.headers.get("content-type", ""), url)
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(r.content)
        tmp_path = tmp.name

    try:
        result = await client.upload_image(tmp_path)
        return result.url
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def _guess_ext(content_type: str, url: str) -> str:
    mime_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
    }
    ct = content_type.split(";")[0].strip()
    if ct in mime_map:
        return mime_map[ct]
    # fallback: extract from URL
    from urllib.parse import urlparse

    parsed = urlparse(url)
    p = Path(parsed.path)
    return p.suffix if p.suffix in (".jpg", ".jpeg", ".png", ".gif", ".webp") else ".jpg"
