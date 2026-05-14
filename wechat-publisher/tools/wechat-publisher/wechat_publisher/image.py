import tempfile
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx

from .client import WeChatClient


class AssetProcessingError(RuntimeError):
    """Raised when markdown assets are not ready for WeChat publishing."""


_PLACEHOLDER_RE = re.compile(r"\[插图：.+?\]|\[绘图提示：.+?\]")
_MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_WECHAT_IMAGE_HOSTS = {"mmbiz.qpic.cn", "mmbiz.qlogo.cn"}


async def prepare_markdown_assets(
    md: str,
    client: Any,
    base_dir: Path | None = None,
) -> str:
    """Upload markdown images to WeChat CDN and reject unresolved placeholders."""
    match = _PLACEHOLDER_RE.search(md)
    if match:
        raise AssetProcessingError(
            f"未解析插图占位符：{match.group(0)}。请先生成图片并用 Markdown 图片语法插入。"
        )

    replacements: list[tuple[int, int, str]] = []
    for image in _MARKDOWN_IMAGE_RE.finditer(md):
        src = image.group(2).strip()
        uploaded_url = await _upload_markdown_image(client, src, base_dir)
        if not uploaded_url:
            continue
        replacements.append((image.start(2), image.end(2), uploaded_url))

    if not replacements:
        return md

    parts: list[str] = []
    cursor = 0
    for start, end, replacement in replacements:
        parts.append(md[cursor:start])
        parts.append(replacement)
        cursor = end
    parts.append(md[cursor:])
    return "".join(parts)


async def _upload_markdown_image(
    client: Any,
    src: str,
    base_dir: Path | None,
) -> str | None:
    parsed = urlparse(src)
    if parsed.scheme in {"http", "https"}:
        if parsed.hostname in _WECHAT_IMAGE_HOSTS:
            return None
        return await upload_image_from_url(client, src)

    if parsed.scheme:
        return None

    image_path = Path(src).expanduser()
    if not image_path.is_absolute() and base_dir is not None:
        image_path = base_dir / image_path
    if not image_path.exists():
        raise AssetProcessingError(f"图片文件不存在：{image_path}")

    result = await client.upload_image(str(image_path))
    return result.url


async def upload_image_from_url(client: WeChatClient, url: str) -> str:
    """Download image from *url*, upload to WeChat CDN, return WeChat URL."""
    async with httpx.AsyncClient(timeout=30) as http:
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
    parsed = urlparse(url)
    p = Path(parsed.path)
    return p.suffix if p.suffix in (".jpg", ".jpeg", ".png", ".gif", ".webp") else ".jpg"
