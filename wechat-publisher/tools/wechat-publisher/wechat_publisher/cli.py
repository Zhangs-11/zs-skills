import argparse
import asyncio
import re
import sys
from pathlib import Path

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
    settings = Settings()
    client = WeChatClient(settings)

    cmd = args.command

    if cmd == "upload-image":
        result = await client.upload_image(args.file)
        print(f"SUCCESS: Image uploaded → {result.url}")
        return

    if cmd == "upload-cover":
        media_id = await client.upload_cover(args.file)
        print(f"SUCCESS: Cover uploaded (media_id={media_id})")
        return

    # create / update → read markdown and make assets publish-ready
    md, base_dir = _read_content(args)
    md = await prepare_markdown_assets(md, client, base_dir=base_dir)

    html = markdown_to_wechat_html(md)
    digest = args.digest or _derive_digest(md)
    show_cover_pic = 1 if args.show_cover_pic else 0
    cover_media_id = await _resolve_cover_media_id(client, args)

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
    if args.cover_file and args.cover_media_id:
        raise ValueError("Choose either --cover-file or --cover-media-id, not both.")
    if args.cover_file:
        return await client.upload_cover(args.cover_file)
    return args.cover_media_id


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
