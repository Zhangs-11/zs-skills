"""Read-only validation for external links referenced by an article."""

from __future__ import annotations

import asyncio
import re
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from .secure_download import SecureDownloadError, check_public_url_status

_RAW_URL_RE = re.compile(r"(?i)https?://[^\s<>\]\[\"'“”‘’，。；：！？、]+")
_TRAILING_PUNCTUATION = "，。；：！？、,.!?;:）"


def extract_external_links(md: str) -> list[str]:
    urls: set[str] = set()
    for token in MarkdownIt("commonmark").parse(md):
        if token.type == "html_block":
            _add_html_links(urls, token.content)
            continue
        if token.type != "inline":
            continue
        for child in token.children or []:
            if child.type == "link_open":
                href = child.attrGet("href")
                if href and href.lower().startswith(("http://", "https://")):
                    urls.add(href)
            elif child.type == "text":
                for match in _RAW_URL_RE.finditer(child.content):
                    urls.add(_trim_bare_url(match.group(0)))
            elif child.type == "html_inline":
                _add_html_links(urls, child.content)
    return sorted(urls)


async def check_external_links(md: str, *, timeout: float = 8.0) -> list[str]:
    findings: list[str] = []
    for url in extract_external_links(md):
        try:
            status = await asyncio.to_thread(check_public_url_status, url, timeout=timeout)
        except SecureDownloadError as exc:
            findings.append(f"外链无法安全验证：{url}（{exc}）")
            continue
        if status >= 400 and status not in {401, 403, 405, 429}:
            findings.append(f"外链返回 HTTP {status}：{url}")
    return findings


def _trim_bare_url(url: str) -> str:
    trimmed = url.rstrip(_TRAILING_PUNCTUATION)
    while trimmed.endswith(")") and trimmed.count(")") > trimmed.count("("):
        trimmed = trimmed[:-1]
    return trimmed


def _add_html_links(urls: set[str], html: str) -> None:
    soup = BeautifulSoup(html, "html.parser")
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"])
        if href.lower().startswith(("http://", "https://")):
            urls.add(href)
