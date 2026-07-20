#!/usr/bin/env python3
"""Generate WeChat article images from markdown placeholders via SiliconFlow."""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import tempfile
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from PIL import Image
from wechat_publisher.secure_download import SecureDownloadError, download_public_url

API_BASE = "https://api.siliconflow.cn/v1"
MODEL = "Tongyi-MAI/Z-Image-Turbo"
# auto 兜底通道用它把中文段落转成英文视觉概念（避免中文被画进图里变错别字）
CHAT_MODEL = "deepseek-ai/DeepSeek-V3"  # 概念生成比 7B 小模型稳得多，不易出乱码/串语种
IMAGE_SIZE = "1024x1024"
COVER_IMAGE_SIZE = "1280x720"  # 微信文章封面横版比例
JPEG_QUALITY = 85  # 肉眼无损阈值，比 PNG 体积小 60-70%
MAX_GENERATED_IMAGE_BYTES = 20 * 1024 * 1024
MAX_GENERATED_IMAGE_PIXELS = 40_000_000
SUPPORTED_GENERATED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

# 配图统一创作方向：用比喻/概念表达语义，画面里绝不出现任何文字（根治错别字）
CREATIVE_DIRECTION = (
    "Express the idea through visual metaphor and symbolism, not by writing it out. "
    "Modern flat editorial illustration for an AI-technology article, one strong focal "
    "concept, clean composition, limited blue-centered palette, generous negative space, "
    "tasteful and a little imaginative. "
    "IMPORTANT: Do NOT depict whiteboards, blackboards, flowcharts, mind maps, diagrams, "
    "text boxes, bullet lists, screens showing text, sticky notes, signs, or any scene "
    "that naturally contains written words — these always produce garbled characters. "
    "Use abstract shapes, natural scenery, objects, or people instead. "
    "Absolutely no text of any kind: no words, no letters, no Chinese characters, no "
    "numbers, no captions, no labels, no watermark, no logo anywhere in the image."
)

# 负向词：进一步压制模型把文字画进图里
NEGATIVE_PROMPT = (
    "text, words, letters, captions, subtitles, label, typography, chinese characters, "
    "japanese characters, korean characters, numbers, digits, watermark, logo, signature, "
    "ui, interface, gibberish, misspelled text, garbled text, blurry, low quality, deformed"
)

PLACEHOLDER_RE = re.compile(
    r"(?P<placeholder>\[插图：(?P<description>.+?)\]\s*\n"
    r"\[绘图提示：(?P<prompt>.+?)\])",
    re.DOTALL,
)
GENERATED_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(images/(?:[^/)\s]+/)?\d{2}-[^)\s]+\.(?:png|jpe?g|gif|webp)\)",
    re.IGNORECASE,
)
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


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
                filename=f"{index:02d}-{_slugify(description)}.jpg",
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
        "negative_prompt": NEGATIVE_PROMPT,
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
    # 每篇文章用以文件名命名的独立子目录，避免多篇共用 images/ 时同名图互相覆盖
    output_dir = image_dir or article_path.parent / "images" / article_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    relative_image_dir = _relative_path(output_dir, article_path.parent)
    generate = generator or generate_one_image

    generated_paths: list[Path] = []
    requests = extract_image_requests(md)
    if not requests and auto_insert > 0:
        if not _contains_image_from_directory(md, relative_image_dir):
            md, requests = auto_insert_image_requests(
                md,
                count=auto_insert,
                api_key=api_key,
                api_base=api_base,
            )

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

    updated = replace_placeholders(md, requests, relative_image_dir) if requests else md

    cover_path = output_dir / "cover.jpg"
    generate(
        cover_prompt or _cover_prompt(title, md, api_key=api_key, api_base=api_base),
        cover_path,
        api_key=api_key,
        api_base=api_base,
        model=model,
        image_size=COVER_IMAGE_SIZE,
    )

    # 正文最后写入：若封面失败，文章仍保持原样，避免留下只生成一半的草稿。
    if requests:
        temp_article: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=article_path.parent,
                prefix=f".{article_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as tmp:
                temp_article = Path(tmp.name)
                tmp.write(updated)
            temp_article.replace(article_path)
        finally:
            if temp_article is not None:
                temp_article.unlink(missing_ok=True)

    return {"images": generated_paths, "cover": cover_path}


def auto_insert_image_requests(
    md: str,
    *,
    count: int = 3,
    api_key: str | None = None,
    api_base: str = API_BASE,
) -> tuple[str, list[ImageRequest]]:
    if GENERATED_IMAGE_RE.search(md):
        return md, []
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
        prompt = _auto_image_prompt(paragraph, api_key=api_key, api_base=api_base)
        filename = f"{image_index:02d}-image.jpg"
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
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"SiliconFlow image generation failed ({exc.code}): {body}") from exc

    image_url = _extract_image_url(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        downloaded = download_public_url(
            image_url,
            max_bytes=MAX_GENERATED_IMAGE_BYTES,
            supported_content_types=SUPPORTED_GENERATED_IMAGE_TYPES,
            require_https=True,
        )
    except SecureDownloadError as exc:
        raise RuntimeError(str(exc)) from exc
    image_bytes = downloaded.body
    if not _has_supported_image_signature(image_bytes):
        raise RuntimeError("Downloaded file is not a valid image.")

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".jpg",
            delete=False,
        ) as tmp:
            temp_path = Path(tmp.name)
        _save_as_jpeg(image_bytes, temp_path)
        temp_path.replace(output_path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def _extract_image_url(data: dict[str, object]) -> str:
    images = data.get("images")
    if not isinstance(images, list) or not images:
        raise RuntimeError(f"SiliconFlow response did not contain images: {data}")
    first = images[0]
    if not isinstance(first, dict) or not isinstance(first.get("url"), str):
        raise RuntimeError(f"SiliconFlow image item did not contain url: {data}")
    return first["url"]


def _save_as_jpeg(image_bytes: bytes, output_path: Path) -> None:
    with Image.open(io.BytesIO(image_bytes)) as img:
        if img.width * img.height > MAX_GENERATED_IMAGE_PIXELS:
            raise RuntimeError("Generated image exceeds the decoded pixel limit.")
        img.load()
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def _has_supported_image_signature(image_bytes: bytes) -> bool:
    header = image_bytes[:12]
    return (
        header.startswith(b"\x89PNG\r\n\x1a\n")
        or header.startswith(b"\xff\xd8\xff")
        or header.startswith((b"GIF87a", b"GIF89a"))
        or (header.startswith(b"RIFF") and header[8:12] == b"WEBP")
    )


def _article_image_prompt(prompt: str) -> str:
    # 作者在 [绘图提示] 里手写的英文创意概念，直接作为画面主体，再叠加统一创作方向
    return f"{prompt}. {CREATIVE_DIRECTION}"


def _auto_image_prompt(
    paragraph: str,
    *,
    api_key: str | None = None,
    api_base: str = API_BASE,
) -> str:
    # 兜底通道：先把中文段落转成英文视觉概念，绝不把中文塞进生图 prompt
    # （只要 prompt 里出现中文，模型就会把它画成图上的错别字）。
    concept = _summarize_concept_en(_theme_seed(paragraph), api_key, api_base)
    if not concept:
        concept = (
            "an abstract idea from a modern AI and large-language-model technology article, "
            "shown through symbolic motifs like flowing data streams, light, funnels, "
            "layered blocks or neural threads"
        )
    return f"{concept}. {CREATIVE_DIRECTION}"


def _theme_seed(paragraph: str) -> str:
    clean = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", paragraph)
    clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
    clean = re.sub(r"[*_`>#-]+", "", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean[:160]


def _summarize_concept_en(
    theme: str,
    api_key: str | None,
    api_base: str = API_BASE,
) -> str | None:
    """用对话模型把中文主题转成一句英文视觉概念；任何失败都返回 None 走通用兜底。"""
    key = api_key or os.environ.get("SILICONFLOW_API_KEY")
    if not key or not theme:
        return None
    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You turn a Chinese sentence from an AI-technology article into ONE short "
                    "English prompt describing a single concrete visual scene (objects, colors, "
                    "action) that metaphorically conveys its meaning. Max 25 words. "
                    "No technical jargon, no numbers, no math notation, no Chinese, no quotes. "
                    "No brand names, no acronyms (like AI, GPT, LLM), no abbreviations, no text or "
                    "letters in the scene. Output only the visual description."
                ),
            },
            {"role": "user", "content": theme},
        ],
        "temperature": 0.7,
        "max_tokens": 90,
    }
    try:
        req = urllib.request.Request(
            f"{api_base.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"].strip()
        # 兜底清洗：去掉任何残留中文字符，确保不把中文带进生图 prompt
        text = re.sub(r"[一-鿿]+", " ", text)
        text = _strip_acronyms(text)
        text = re.sub(r"\s+", " ", text).strip().strip('"').strip()
        return text or None
    except Exception:
        return None


def _strip_acronyms(text: str) -> str:
    """去掉独立的全大写缩写（AI、GPT、LLM、API 等），避免被生图模型当文字画到图上。"""
    return re.sub(r"\b[A-Z]{2,5}\b", " ", text)


def _cover_prompt(
    title: str,
    md: str,
    *,
    api_key: str | None = None,
    api_base: str = API_BASE,
) -> str:
    # 封面加固：用标题 + 正文多段采样生成主题，避免开头套话导致不同文章封面雷同。
    # 标题原文不直接进画面（含 AI 等缩写易被画成文字），先转成纯英文视觉概念。
    seed = _cover_theme_seed(title, md)
    concept = _summarize_concept_en(seed, api_key, api_base)
    if not concept:
        concept = (
            "a bold central metaphor for a modern technology breakthrough, "
            "such as a vast field of light converging into one bright focal point"
        )
    return (
        f"A single bold symbolic illustration: {concept}. "
        "One strong focal subject that reads well as a small mobile thumbnail, "
        "premium and a little surprising. "
        f"{CREATIVE_DIRECTION}"
    )


def _cover_theme_seed(title: str, md: str, limit: int = 300) -> str:
    """标题 + 正文首/中/尾三段采样，让每篇封面主题足够独特。"""
    def clean(text: str) -> str:
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"[*_`>#=|\-]+", "", text)
        return re.sub(r"\s+", " ", text).strip()

    blocks = [clean(b) for b in re.split(r"\n\s*\n", md) if _is_content_paragraph(b)]
    if not blocks:
        return clean(title)

    indices = _spread_indexes(list(range(len(blocks))), min(3, len(blocks)))
    sampled = " ".join(blocks[i] for i in indices)
    seed = f"{clean(title)}. {sampled}"
    return seed[:limit]


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


def _contains_image_from_directory(md: str, image_dir: Path) -> bool:
    expected = image_dir.as_posix().rstrip("/") + "/"
    return any(
        match.group(1).split("?", 1)[0].startswith(expected)
        for match in MARKDOWN_IMAGE_RE.finditer(md)
    )


def _is_content_paragraph(block: str) -> bool:
    text = block.strip()
    if len(text) < 15:
        return False
    if text.startswith(
        (
            "#",
            "![",
            "[插图：",
            "[绘图提示：",
            "---",
            "|",
            ">",
            "```",
            "~~~",
        )
    ):
        return False
    if text.startswith(("> / 作者：", "> / 投稿或爆料")):
        return False
    return True


def _spread_indexes(indexes: list[int], count: int) -> list[int]:
    if count <= 0 or not indexes:
        return []
    count = min(count, len(indexes))
    if count == 1:
        return [indexes[min(1, len(indexes) - 1)]]
    # 直接在可用位置的首尾间等距取样，保证数量准确且不重复。
    return [
        indexes[round(i * (len(indexes) - 1) / (count - 1))]
        for i in range(count)
    ]


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
