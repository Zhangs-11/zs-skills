import argparse
import asyncio
import sys

from .client import WeChatClient
from .config import Settings
from .formatter import markdown_to_wechat_html


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
    asyncio.run(_dispatch(args))


def _add_content_args(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content-file", "-f", help="Read markdown from file")
    group.add_argument("--stdin", "-s", action="store_true", help="Read markdown from stdin")


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

    # create / update → read markdown
    md = _read_content(args)

    html = markdown_to_wechat_html(md)

    if cmd == "create":
        result = await client.create_draft(args.title, html)
        print(f"SUCCESS: Draft created (media_id={result.media_id})")
    elif cmd == "update":
        result = await client.update_draft(args.media_id, args.title, html)
        print(f"SUCCESS: Draft updated (media_id={result.media_id})")


def _read_content(args: argparse.Namespace) -> str:
    if args.content_file:
        with open(args.content_file, encoding="utf-8") as f:
            return f.read()
    if args.stdin or not sys.stdin.isatty():
        return sys.stdin.read()
    raise RuntimeError("No input provided")
