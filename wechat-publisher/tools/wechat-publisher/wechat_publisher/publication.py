"""Contract between an editable mother draft and its publishable body."""

from __future__ import annotations

import re
from dataclasses import dataclass

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt


DELIVERY_APPENDIX_MARKER = "<!-- kakarot:delivery-appendix -->"
_FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.DOTALL)
_YAML_KEY_RE = re.compile(r"(?m)^\s*(?:\"[^\"]+\"|'[^']+'|[^\s:#][^:]*)\s*:")
_INTERNAL_HEADINGS = {"截图清单", "封面文件", "封面方案", "备选标题", "事实确认项", "交付说明"}


@dataclass(frozen=True)
class PublicationDocument:
    public_markdown: str
    delivery_appendix: str
    had_frontmatter: bool


def split_publication_document(md: str) -> PublicationDocument:
    """Remove metadata and split the explicit non-publishable delivery appendix."""
    normalized = md.lstrip("\ufeff").replace("\r\n", "\n")
    candidate = _FRONTMATTER_RE.match(normalized)
    frontmatter = candidate if candidate and _YAML_KEY_RE.search(candidate.group(1)) else None
    had_frontmatter = frontmatter is not None
    if frontmatter:
        normalized = normalized[frontmatter.end() :]

    marker_lines = _delivery_marker_lines(normalized)
    lines = normalized.splitlines(keepends=True)
    marker_line = marker_lines[0] if marker_lines else None
    public = "".join(lines[:marker_line]) if marker_line is not None else normalized
    appendix = "".join(lines[marker_line + 1 :]) if marker_line is not None else ""
    return PublicationDocument(
        public_markdown=public.strip() + "\n" if public.strip() else "",
        delivery_appendix=appendix.strip(),
        had_frontmatter=had_frontmatter,
    )


def publication_contract_findings(*, title: str, md: str) -> list[str]:
    document = split_publication_document(md)
    findings: list[str] = []
    headings = _markdown_headings(document.public_markdown)
    h1 = next((text for level, text in headings if level == 1), None)
    if h1:
        if _normalize_title(h1) == _normalize_title(title):
            findings.append("正文重复了发布标题；删除正文中的一级标题")
        else:
            findings.append("正文含一级标题；公众号标题由 --title 单独传入")
    internal_heading = next(
        (text for level, text in headings if level >= 2 and _is_internal_heading(text)),
        None,
    )
    if internal_heading:
        findings.append(
            f"内部交付内容“{internal_heading}”进入正文；"
            f"请放到 {DELIVERY_APPENDIX_MARKER} 之后"
        )
    if not document.public_markdown.strip():
        findings.append("可发布正文为空")
    return findings


def _normalize_title(value: str) -> str:
    return re.sub(r"[\s‘’“”\"'《》【】]", "", value).casefold()


def _markdown_headings(md: str) -> list[tuple[int, str]]:
    tokens = MarkdownIt("commonmark").parse(md)
    headings: list[tuple[int, str]] = []
    for index, token in enumerate(tokens[:-1]):
        if token.type != "heading_open":
            continue
        inline = tokens[index + 1]
        if inline.type == "inline":
            headings.append((int(token.tag[1:]), inline.content.strip()))
        continue
    for token in tokens:
        if token.type == "inline":
            html = token.content if any(
                child.type == "html_inline" for child in token.children or []
            ) else ""
        elif token.type == "html_block":
            html = token.content
        else:
            continue
        if "<h" not in html.lower():
            continue
        soup = BeautifulSoup(html, "html.parser")
        for level in range(1, 7):
            headings.extend((level, item.get_text(" ", strip=True)) for item in soup.find_all(f"h{level}"))
    return headings


def _delivery_marker_lines(md: str) -> list[int]:
    lines: list[int] = []
    for token in MarkdownIt("commonmark").parse(md):
        if (
            token.type == "html_block"
            and token.level == 0
            and token.content.strip() == DELIVERY_APPENDIX_MARKER
            and token.map is not None
        ):
            lines.append(token.map[0])
    return lines


def _is_internal_heading(text: str) -> bool:
    normalized = re.sub(r"[\s：:（(].*$", "", text.strip())
    return normalized in _INTERNAL_HEADINGS
