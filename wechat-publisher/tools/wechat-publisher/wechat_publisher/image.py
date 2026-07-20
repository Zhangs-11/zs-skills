import asyncio
import ipaddress
import socket
import tempfile
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .client import WeChatClient
from .secure_download import SecureDownloadError, download_public_url


class AssetProcessingError(RuntimeError):
    """Raised when markdown assets are not ready for WeChat publishing."""


_PLACEHOLDER_RE = re.compile(r"\[插图：.+?\]|\[绘图提示：.+?\]")
_MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_WECHAT_IMAGE_HOSTS = {"mmbiz.qpic.cn", "mmbiz.qlogo.cn"}
_SUPPORTED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_REMOTE_IMAGE_BYTES = 10 * 1024 * 1024


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
    tmp_path: str | None = None
    try:
        try:
            downloaded = await asyncio.to_thread(
                download_public_url,
                url,
                max_bytes=MAX_REMOTE_IMAGE_BYTES,
                supported_content_types=_SUPPORTED_IMAGE_TYPES,
            )
        except SecureDownloadError as exc:
            raise AssetProcessingError(str(exc)) from exc
        ext = _guess_ext(downloaded.content_type, url)
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(downloaded.body)
        result = await client.upload_image(tmp_path)
        return result.url
    finally:
        if tmp_path is not None:
            Path(tmp_path).unlink(missing_ok=True)


def _validate_remote_image_url(
    url: str,
) -> set[ipaddress.IPv4Address | ipaddress.IPv6Address]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise AssetProcessingError(f"不支持的远程图片地址：{url}")
    try:
        port = parsed.port
    except ValueError as exc:
        raise AssetProcessingError(f"不支持的远程图片地址：{url}") from exc
    if port not in (None, 80, 443):
        raise AssetProcessingError("remote image uses an unsupported port")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise AssetProcessingError("remote image points to a private or local address")
    try:
        addresses = [ipaddress.ip_address(hostname)]
    except ValueError:
        try:
            addresses = [
                ipaddress.ip_address(item[4][0])
                for item in socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
            ]
        except socket.gaierror as exc:
            raise AssetProcessingError(f"远程图片域名无法解析：{hostname}") from exc
    if any(not _is_public_address(address) for address in addresses):
        raise AssetProcessingError("remote image points to a private or local address")
    return set(addresses)


def _is_public_address(
    address: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> bool:
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_unspecified
        or address.is_multicast
    )


def _validate_remote_image_response(
    content_type: str,
    *,
    content_length: int | None,
) -> None:
    normalized = content_type.split(";", 1)[0].strip().lower()
    if normalized not in _SUPPORTED_IMAGE_TYPES:
        raise AssetProcessingError(f"unsupported remote image content type: {content_type or 'missing'}")
    if content_length is not None and content_length > MAX_REMOTE_IMAGE_BYTES:
        raise AssetProcessingError("remote image is too large")


def _parse_content_length(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        length = int(value)
    except ValueError as exc:
        raise AssetProcessingError("invalid remote image content length") from exc
    if length < 0:
        raise AssetProcessingError("invalid remote image content length")
    return length


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
