import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from .client import WeChatAPIError, WeChatClient
from .config import Settings
from .formatter import markdown_to_wechat_html
from .image import AssetProcessingError, prepare_markdown_assets


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wechat-publisher",
        description="Markdown → WeChat Official Account draft publisher",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- create ---
    create = sub.add_parser("create", help="Create a new draft")
    create.add_argument("--title", "-t", required=True)
    _add_content_args(create)

    # --- update ---
    update = sub.add_parser("update", help="Update an existing draft")
    update.add_argument("--media-id", "-m", required=True)
    update.add_argument("--title", "-t", required=True)
    _add_content_args(update)

    # --- upload-image ---
    upload = sub.add_parser("upload-image", help="Upload an image to WeChat CDN")
    upload.add_argument("file", help="Path to the image file")

    # --- upload-cover ---
    cover = sub.add_parser("upload-cover", help="Upload a cover image and get media_id")
    cover.add_argument("file", help="Path to the cover image file")

    # --- preflight ---
    preflight = sub.add_parser("preflight", help="Validate an article without uploading it")
    preflight.add_argument("--title", "-t", required=True)
    _add_content_args(preflight)

    args = parser.parse_args()
    try:
        asyncio.run(_dispatch(args))
    except WeChatAPIError as exc:
        if exc.code == 40164:
            print(
                "ERROR: IP is not in the WeChat API whitelist. "
                "Run `curl -s ip.sb`, then add that IP in mp.weixin.qq.com → "
                "开发 → 基本配置 → IP 白名单.",
                file=sys.stderr,
            )
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    except (AssetProcessingError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def _add_content_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content-file", "-f", help="Read markdown from file")
    group.add_argument("--stdin", "-s", action="store_true", help="Read markdown from stdin")
    parser.add_argument("--cover-media-id", help="Override WECHAT_DEFAULT_COVER_MEDIA_ID")
    parser.add_argument("--cover-file", help="Upload this cover image before publishing")
    parser.add_argument("--digest", help="Article digest shown in WeChat feeds")
    parser.add_argument("--source-url", help="Original source URL for the article")
    parser.add_argument(
        "--show-cover-pic",
        action="store_true",
        help="Show cover image at the top of the article body",
    )


async def _dispatch(args: argparse.Namespace) -> None:
    cmd = args.command

    if cmd == "preflight":
        md, base_dir = _read_content(args)
        findings = _preflight_findings(
            title=args.title,
            md=md,
            base_dir=base_dir,
            cover_file=args.cover_file,
            cover_media_id=args.cover_media_id,
        )
        if findings:
            raise AssetProcessingError("；".join(findings))
        html = markdown_to_wechat_html(md)
        print(f"PREFLIGHT: OK (html_chars={len(html)})")
        return

    settings = Settings()
    client = WeChatClient(settings)

    if cmd == "upload-image":
        result = await client.upload_image(args.file)
        print(f"SUCCESS: Image uploaded → {result.url}")
        return

    if cmd == "upload-cover":
        media_id = await client.upload_cover(args.file)
        print(f"SUCCESS: Cover uploaded (media_id={media_id})")
        return

    # create / update：先完成所有本地验证，再发生任何上传，避免失败命令消耗素材配额。
    _validate_cover_selection(args)
    md, base_dir = _read_content(args)
    findings = _preflight_findings(
        title=args.title,
        md=md,
        base_dir=base_dir,
        cover_file=args.cover_file,
        cover_media_id=args.cover_media_id,
    )
    if findings:
        raise AssetProcessingError("；".join(findings))
    markdown_to_wechat_html(md)  # 先验证 Markdown 可格式化；此时不上传任何内容。

    cover_media_id = await _resolve_cover_media_id(client, args)
    if cmd == "create" and not cover_media_id:
        cover_media_id = settings.wechat_default_cover_media_id or None
        if not cover_media_id:
            raise ValueError(
                "cover media_id is required. Set WECHAT_DEFAULT_COVER_MEDIA_ID, "
                "pass --cover-media-id, or pass --cover-file."
            )
    elif cmd == "update" and not cover_media_id:
        cover_media_id = await client.get_draft_cover(args.media_id)
        if not cover_media_id:
            raise ValueError("existing draft does not contain a usable cover media_id")

    md = await prepare_markdown_assets(md, client, base_dir=base_dir)

    html = markdown_to_wechat_html(md)
    digest = args.digest or _derive_digest(md)
    show_cover_pic = 1 if args.show_cover_pic else 0

    if cmd == "create":
        result = await client.create_draft(
            args.title,
            html,
            cover_media_id=cover_media_id,
            digest=digest,
            content_source_url=args.source_url,
            show_cover_pic=show_cover_pic,
        )
        print(f"SUCCESS: Draft created (media_id={result.media_id})")
    elif cmd == "update":
        result = await client.update_draft(
            args.media_id,
            args.title,
            html,
            cover_media_id=cover_media_id,
            digest=digest,
            content_source_url=args.source_url,
            show_cover_pic=show_cover_pic,
        )
        print(f"SUCCESS: Draft updated (media_id={result.media_id})")


async def _resolve_cover_media_id(
    client: WeChatClient,
    args: argparse.Namespace,
) -> str | None:
    if args.cover_file:
        return await client.upload_cover(args.cover_file)
    return args.cover_media_id


def _validate_cover_selection(args: argparse.Namespace) -> None:
    if args.cover_file and args.cover_media_id:
        raise ValueError("Choose either --cover-file or --cover-media-id, not both.")


def _read_content(args: argparse.Namespace) -> tuple[str, Path | None]:
    if args.content_file:
        path = Path(args.content_file).expanduser()
        with open(path, encoding="utf-8") as f:
            return f.read(), path.parent
    if args.stdin or not sys.stdin.isatty():
        return sys.stdin.read(), None
    raise RuntimeError("No input provided")


def _derive_digest(md: str, limit: int = 120) -> str:
    for block in re.split(r"\n\s*\n", md):
        text = block.strip()
        if not text or text.startswith(("#", "![", "[插图：", "[绘图提示：")):
            continue
        text = _strip_markdown(text)
        if not text:
            continue
        return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"
    return ""


def _strip_markdown(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`>#-]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _preflight_findings(
    *,
    title: str,
    md: str,
    base_dir: Path | None,
    cover_file: str | None,
    cover_media_id: str | None,
) -> list[str]:
    findings: list[str] = []
    if not title.strip():
        findings.append("标题不能为空")
    placeholder = re.search(r"\[插图：.+?\]|\[绘图提示：.+?\]", md)
    if placeholder:
        findings.append(f"存在未解析插图占位符：{placeholder.group(0)}")
    for image in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", md):
        src = image.group(1).strip()
        parsed = urlparse(src)
        if parsed.scheme in {"http", "https"}:
            continue
        if parsed.scheme:
            findings.append(f"图片使用了不支持的地址：{src}")
            continue
        path = Path(src).expanduser()
        if not path.is_absolute() and base_dir is not None:
            path = base_dir / path
        if not path.is_file() or not os.access(path, os.R_OK):
            findings.append(f"图片文件不存在：{path}")
    if cover_file and cover_media_id:
        findings.append("封面文件与封面 media_id 只能选择一个")
    elif cover_file:
        cover_path = Path(cover_file).expanduser()
        if not cover_path.is_file() or not os.access(cover_path, os.R_OK):
            findings.append(f"封面文件不存在：{cover_path}")
    return findings
