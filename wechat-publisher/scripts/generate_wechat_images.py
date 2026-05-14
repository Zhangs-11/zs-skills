#!/usr/bin/env python3
"""Generate WeChat article images from markdown placeholders via SiliconFlow."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

API_BASE = "https://api.siliconflow.cn/v1"
MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
IMAGE_SIZE = "1024x1024"

PLACEHOLDER_RE = re.compile(
    r"(?P<placeholder>\[插图：(?P<description>.+?)\]\s*\n"
    r"\[绘图提示：(?P<prompt>.+?)\])",
    re.DOTALL,
)


@dataclass(frozen=True)
class ImageRequest:
    description: str
    prompt: str
    filename: str
    placeholder: str


def extract_image_requests(md: str) -> list[ImageRequest]:
    requests: list[ImageRequest] = []
    for index, match in enumerate(PLACEHOLDER_RE.finditer(md), start=1):
        description = " ".join(match.group("description").split())
        prompt = " ".join(match.group("prompt").split())
        requests.append(
            ImageRequest(
                description=description,
                prompt=prompt,
                filename=f"{index:02d}-{_slugify(description)}.png",
                placeholder=match.group("placeholder"),
            )
        )
    return requests


def replace_placeholders(
    md: str,
    requests: Iterable[ImageRequest],
    image_dir: Path,
) -> str:
    updated = md
    for item in requests:
        updated = updated.replace(
            item.placeholder,
            f"![{item.description}]({image_dir.as_posix()}/{item.filename})",
        )
    return updated


def build_generation_payload(
    prompt: str,
    *,
    model: str = MODEL,
    image_size: str = IMAGE_SIZE,
) -> dict[str, object]:
    return {
        "model": model,
        "prompt": prompt,
        "image_size": image_size,
        "batch_size": 1,
        "num_inference_steps": 28,
        "guidance_scale": 7.5,
    }


def generate_article_images(
    article_path: Path,
    *,
    title: str,
    generator: Callable[..., None] = None,
    image_dir: Path | None = None,
    cover_prompt: str | None = None,
    auto_insert: int = 3,
    api_key: str | None = None,
    api_base: str = API_BASE,
    model: str = MODEL,
    image_size: str = IMAGE_SIZE,
) -> dict[str, list[Path] | Path]:
    md = article_path.read_text(encoding="utf-8")
    output_dir = image_dir or article_path.parent / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    relative_image_dir = _relative_path(output_dir, article_path.parent)
    generate = generator or generate_one_image

    generated_paths: list[Path] = []
    requests = extract_image_requests(md)
    if not requests and auto_insert > 0:
        md, requests = auto_insert_image_requests(md, count=auto_insert)

    for item in requests:
        output_path = output_dir / item.filename
        generate(
            _article_image_prompt(item.prompt),
            output_path,
            api_key=api_key,
            api_base=api_base,
            model=model,
            image_size=image_size,
        )
        generated_paths.append(output_path)

    if requests:
        updated = replace_placeholders(md, requests, relative_image_dir)
        article_path.write_text(updated, encoding="utf-8")

    cover_path = output_dir / "cover.png"
    generate(
        cover_prompt or _cover_prompt(title, md),
        cover_path,
        api_key=api_key,
        api_base=api_base,
        model=model,
        image_size=image_size,
    )

    return {"images": generated_paths, "cover": cover_path}


def auto_insert_image_requests(
    md: str,
    *,
    count: int = 3,
) -> tuple[str, list[ImageRequest]]:
    blocks = re.split(r"(\n\s*\n)", md)
    paragraph_indexes = [
        idx
        for idx, block in enumerate(blocks)
        if _is_content_paragraph(block)
    ]
    if not paragraph_indexes:
        return md, []

    selected = _spread_indexes(paragraph_indexes, min(count, len(paragraph_indexes)))
    inserted = list(blocks)
    requests: list[ImageRequest] = []
    offset = 0
    for image_index, block_index in enumerate(selected, start=1):
        paragraph = blocks[block_index].strip()
        description = f"配图{image_index}"
        prompt = _auto_image_prompt(paragraph)
        filename = f"{image_index:02d}-image.png"
        markdown_image = f"\n\n![{description}](images/{filename})"
        inserted_at = block_index + offset
        inserted[inserted_at] = f"{inserted[inserted_at]}{markdown_image}"
        offset += 0
        requests.append(
            ImageRequest(
                description=description,
                prompt=prompt,
                filename=filename,
                placeholder=markdown_image.strip(),
            )
        )

    return "".join(inserted), requests


def generate_one_image(
    prompt: str,
    output_path: Path,
    *,
    api_key: str | None = None,
    api_base: str = API_BASE,
    model: str = MODEL,
    image_size: str = IMAGE_SIZE,
) -> None:
    resolved_key = api_key or os.environ.get("SILICONFLOW_API_KEY")
    if not resolved_key:
        raise RuntimeError("SILICONFLOW_API_KEY is required for image generation.")

    payload = build_generation_payload(prompt, model=model, image_size=image_size)
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{api_base.rstrip('/')}/images/generations",
        data=body,
        headers={
            "Authorization": f"Bearer {resolved_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.loads(response.read().decode("utf-8"))

    image_url = _extract_image_url(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(image_url, output_path)


def _extract_image_url(data: dict[str, object]) -> str:
    images = data.get("images")
    if not isinstance(images, list) or not images:
        raise RuntimeError(f"SiliconFlow response did not contain images: {data}")
    first = images[0]
    if not isinstance(first, dict) or not isinstance(first.get("url"), str):
        raise RuntimeError(f"SiliconFlow image item did not contain url: {data}")
    return first["url"]


def _article_image_prompt(prompt: str) -> str:
    return (
        f"{prompt}. WeChat official account article illustration, clean AI technology "
        "editorial style, high information density, no watermark, no logo, no readable text."
    )


def _auto_image_prompt(paragraph: str) -> str:
    clean = re.sub(r"[*_`>#-]+", "", paragraph)
    clean = re.sub(r"\s+", " ", clean).strip()
    clean = clean[:220]
    return (
        "Create a clean editorial AI technology illustration for this article idea: "
        f"{clean}. Use abstract product-style diagrams, architecture blocks, "
        "retrieval pipelines, documents, vectors, or knowledge graph motifs where relevant. "
        "No readable text, no logo, no watermark."
    )


def _cover_prompt(title: str, md: str) -> str:
    summary = _first_text_block(md)
    return (
        f"Cover image for a Chinese AI technology WeChat article titled '{title}'. "
        f"Core idea: {summary}. Premium editorial technology visual, strong focal point, "
        "clean composition, suitable for mobile feed thumbnail, no readable text, no logo, no watermark."
    )


def _first_text_block(md: str, limit: int = 160) -> str:
    for block in re.split(r"\n\s*\n", md):
        text = block.strip()
        if not text or text.startswith(("#", "![", "[插图：", "[绘图提示：")):
            continue
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"[*_`>#-]+", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            return text[:limit]
    return title_safe_fallback(md)


def title_safe_fallback(md: str) -> str:
    first_line = next((line.strip("# ").strip() for line in md.splitlines() if line.strip()), "")
    return first_line or "AI technology analysis"


def _slugify(text: str) -> str:
    ascii_words = re.findall(r"[A-Za-z0-9]+", text)
    if ascii_words:
        return "-".join(word.lower() for word in ascii_words[:3])
    return "image"


def _relative_path(path: Path, start: Path) -> Path:
    try:
        return path.relative_to(start)
    except ValueError:
        return Path(os.path.relpath(path, start))


def _is_content_paragraph(block: str) -> bool:
    text = block.strip()
    if len(text) < 15:
        return False
    if text.startswith(("#", "![", "[插图：", "[绘图提示：", "---", "|")):
        return False
    return True


def _spread_indexes(indexes: list[int], count: int) -> list[int]:
    if count <= 0:
        return []
    if count == 1:
        return [indexes[min(1, len(indexes) - 1)]]
    positions = []
    for i in range(count):
        raw = round((i + 1) * (len(indexes) / (count + 1)))
        positions.append(indexes[min(max(raw, 0), len(indexes) - 1)])
    return sorted(dict.fromkeys(positions))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate images for a WeChat markdown article.")
    parser.add_argument("--article", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument("--cover-prompt")
    parser.add_argument("--auto-insert", type=int, default=3)
    parser.add_argument("--api-base", default=API_BASE)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--image-size", default=IMAGE_SIZE)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = generate_article_images(
        args.article.expanduser(),
        title=args.title,
        image_dir=args.image_dir.expanduser() if args.image_dir else None,
        cover_prompt=args.cover_prompt,
        auto_insert=args.auto_insert,
        api_base=args.api_base,
        model=args.model,
        image_size=args.image_size,
    )
    for image in result["images"]:
        print(f"IMAGE: {image}")
    print(f"COVER: {result['cover']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
