import re

from markdown_it import MarkdownIt
from bs4 import BeautifulSoup, NavigableString, Tag

_REMOVE_TAGS = {"style", "script", "iframe", "svg"}
_ACCENT = "#2b6cb0"  # primary accent blue
_ACCENT_LIGHT = "#ebf4ff"  # light blue bg
_TEXT = "#2d3748"
_TEXT_MUTED = "#718096"
_BG_SOFT = "#f7fafc"


def markdown_to_wechat_html(md: str) -> str:
    """Convert markdown to beautifully styled WeChat-compatible HTML."""

    # Pre-process: convert ===highlight=== to <mark> tags（先处理三等号）
    md = re.sub(r"===(.+?)===", r"<mark>\1</mark>", md)
    # 再处理 ==注意小句==：克制的荧光笔下划线（此时三等号已被替换，不会冲突）
    md = re.sub(r"==(.+?)==", r'<mark class="note">\1</mark>', md)

    html = MarkdownIt("commonmark").enable("table").render(md)

    soup = BeautifulSoup(html, "html.parser")

    # Remove unsupported elements
    for tag_name in _REMOVE_TAGS:
        for el in soup.find_all(tag_name):
            el.decompose()

    # --- Paragraphs ---
    for p in soup.find_all("p"):
        _merge_styles(p, _P)
        for child in list(p.children):
            if isinstance(child, str) and child.strip():
                span = soup.new_tag("span")
                span.string = child
                child.replace_with(span)

    # --- Blockquotes ---
    for bq in soup.find_all("blockquote"):
        _merge_styles(bq, _BLOCKQUOTE)
        # Add decorative quote marker
        marker = soup.new_tag("span")
        _merge_styles(marker, _BLOCKQUOTE_MARKER)
        marker.string = "💡"
        bq.insert(0, marker)
        for p in bq.find_all("p"):
            _merge_styles(p, _BLOCKQUOTE_P)

    # --- Headings ---
    for h2 in soup.find_all("h2"):
        _merge_styles(h2, _H2)
        _prepend_heading_icon(h2, _DEFAULT_H2_ICON)

    for h3 in soup.find_all("h3"):
        _merge_styles(h3, _H3)

    # --- Lists ---
    for ul in soup.find_all("ul"):
        _merge_styles(ul, _UL)
    for ol in soup.find_all("ol"):
        _merge_styles(ol, _OL)
    for li in soup.find_all("li"):
        _merge_styles(li, _LI)

    # --- Dividers ---
    for hr in soup.find_all("hr"):
        _wrap_divider(soup, hr)

    # --- Inline text ---
    for strong in soup.find_all("strong"):
        _merge_styles(strong, _STRONG)

    for em in soup.find_all("em"):
        _merge_styles(em, _EM)

    references: list[tuple[int, str, str]] = []
    for a in list(soup.find_all("a")):
        href = a.get("href", "")
        if not href or href.startswith("#"):
            a["style"] = f"color: {_ACCENT}; text-decoration: underline;"
            continue

        number = len(references) + 1
        label = a.get_text(strip=True) or href
        references.append((number, label, href))
        a.replace_with(NavigableString(f"{label}[{number}]"))

    for code in soup.find_all("code"):
        _merge_styles(code, _CODE)

    for pre in soup.find_all("pre"):
        _merge_styles(pre, _PRE)
        for c in pre.find_all("code"):
            _merge_styles(c, _PRE_CODE)

    # --- Styled <mark> ---
    # 普通 ===高亮=== 用 _MARK；==注意小句== (class=note) 用更克制的 _NOTE
    for mark in soup.find_all("mark"):
        classes = mark.get("class") or []
        _merge_styles(mark, _NOTE if "note" in classes else _MARK)
        if mark.has_attr("class"):
            del mark["class"]

    # --- Images ---
    for img in soup.find_all("img"):
        _merge_styles(img, _IMG)
        # try wrapping in a centered container
        parent = img.parent
        if parent and parent.name != "p":
            _wrap_image(soup, img)

    # --- Tables ---
    for table in soup.find_all("table"):
        _merge_styles(table, _TABLE)
        for td in table.find_all("td"):
            _merge_styles(td, _TD)
        for th in table.find_all("th"):
            _merge_styles(th, _TH)

    if references:
        _append_references(soup, references)

    return str(soup)


# ── Style definitions ──────────────────────────────────────────────────

_P = (
    f"margin: 0 0 16px 0; padding: 0;"
    f"font-size: 16px; color: {_TEXT};"
    f"letter-spacing: 1.2px; line-height: 1.85;"
)

# 小标题：左竖线型。无背景，字色与竖线同为主题蓝，字号与正文一致（16px），仅靠加粗+蓝色+竖线区分
_DEFAULT_H2_ICON = "🔹"

_H2 = (
    f"font-size: 16px; font-weight: 700;"
    f"color: {_ACCENT}; margin: 30px 0 14px 0;"
    f"padding: 0 0 0 12px;"
    f"letter-spacing: 1.2px; line-height: 1.85;"
    f"border-left: 4px solid {_ACCENT};"
)

_H3 = (
    f"font-size: 16px; font-weight: 700;"
    f"color: {_ACCENT}; margin: 24px 0 12px 0;"
    f"padding: 0 0 0 10px;"
    f"letter-spacing: 1.2px; line-height: 1.85;"
    f"border-left: 3px solid {_ACCENT};"
)

_BLOCKQUOTE = (
    f"margin: 24px 0; padding: 16px 20px 16px 18px;"
    f"border-left: 4px solid {_ACCENT};"
    f"background-color: {_BG_SOFT};"
    f"border-radius: 0 6px 6px 0;"
    f"font-size: 15px; color: {_TEXT_MUTED};"
    f"letter-spacing: 1px; line-height: 1.7;"
)

_BLOCKQUOTE_MARKER = "display: block; font-size: 16px; margin-bottom: 6px;"

_BLOCKQUOTE_P = (
    f"margin: 0 0 6px 0; padding: 0;"
    f"font-size: 15px; color: {_TEXT_MUTED};"
    f"letter-spacing: 1px; line-height: 1.7;"
)

_UL = (
    f"padding-left: 22px; margin: 10px 0 18px 0;"
    f"font-size: 16px; color: {_TEXT};"
    f"letter-spacing: 1.2px; line-height: 1.85;"
)

_OL = (
    f"padding-left: 24px; margin: 10px 0 18px 0;"
    f"font-size: 16px; color: {_TEXT};"
    f"letter-spacing: 1.2px; line-height: 1.85;"
)

_LI = (
    f"margin-bottom: 8px;"
    f"font-size: 16px; color: {_TEXT};"
    f"letter-spacing: 1.2px; line-height: 1.85;"
)

_STRONG = f"font-weight: 700; color: #1a202c;"

_EM = "font-style: italic;"

_MARK = (
    f"background: linear-gradient(180deg,transparent 60%,{_ACCENT_LIGHT} 60%);"
    f"padding: 0 4px; font-weight: 500; color: {_TEXT};"
)

# ==注意小句== 的轻样式：仅把字变成主题蓝，不加粗
# background:transparent 必须显式写——否则 <mark> 标签会露出默认的黄色底
_NOTE = (
    f"color: {_ACCENT}; background: transparent;"
)

_CODE = (
    f"font-size: 14px; background-color: #edf2f7;"
    f"padding: 2px 8px; border-radius: 4px;"
    f"font-family: 'SF Mono', Menlo, monospace; color: {_TEXT};"
)

_PRE = (
    f"background-color: #1a202c; padding: 18px 20px;"
    f"border-radius: 8px; overflow-x: auto;"
    f"font-size: 14px; line-height: 1.6;"
    f"margin: 20px 0;"
)

_PRE_CODE = (
    f"background: transparent; padding: 0;"
    f"border-radius: 0; color: #e2e8f0;"
    f"font-family: 'SF Mono', Menlo, monospace;"
    f"font-size: 14px;"
)

_IMG = (
    f"max-width: 100%; height: auto;"
    f"border-radius: 8px; margin: 20px auto; display: block;"
)

_TABLE = (
    f"width: 100%; border-collapse: collapse;"
    f"margin: 20px 0; font-size: 15px;"
    f"color: {_TEXT}; line-height: 1.6;"
)

_TD = (
    f"border: 1px solid #e2e8f0; padding: 10px 14px;"
    f"color: {_TEXT};"
)

_TH = (
    f"border: 1px solid #e2e8f0; padding: 10px 14px;"
    f"background-color: {_BG_SOFT}; font-weight: 600;"
    f"color: #1a202c;"
)

# Delicate horizontal rule
_DIVIDER_CONTAINER = (
    f"margin: 36px auto; text-align: center;"
    f"font-size: 13px; color: {_TEXT_MUTED}; letter-spacing: 8px;"
)

# ── Helpers ────────────────────────────────────────────────────────────

def _merge_styles(el: Tag, extra: str) -> None:
    existing = el.get("style", "")
    if existing:
        el["style"] = f"{existing}; {extra}" if not existing.rstrip().endswith(";") else f"{existing} {extra}"
    else:
        el["style"] = extra


# 标题开头若已带 emoji/符号图标，沿用作者写的；否则补一个默认图标
_LEADING_ICON_RE = re.compile(
    "^\\s*[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002190-\U000021FF"
    "\U00002B00-\U00002BFF\U0001F1E6-\U0001F1FF•■-◿✀-➿️]"
)


def _prepend_heading_icon(heading: Tag, icon: str) -> None:
    """If the heading text does not already start with an emoji/icon, prepend one."""
    text = heading.get_text()
    if _LEADING_ICON_RE.match(text):
        return
    heading.insert(0, NavigableString(f"{icon}  "))


def _wrap_divider(soup: BeautifulSoup, hr: Tag) -> None:
    """Replace <hr> with a subtle centered ellipsis."""
    div = soup.new_tag("div")
    div["style"] = _DIVIDER_CONTAINER
    div.string = "· · ·"
    hr.replace_with(div)

def _wrap_image(soup: BeautifulSoup, img: Tag) -> None:
    """Wrap image in a centered container."""
    wrapper = soup.new_tag("div")
    wrapper["style"] = "text-align: center; margin: 20px 0;"
    img.replace_with(wrapper)
    wrapper.append(img)


def _append_references(
    soup: BeautifulSoup,
    references: list[tuple[int, str, str]],
) -> None:
    section = soup.new_tag("section")
    section["style"] = (
        f"margin: 32px 0 0 0; padding-top: 16px;"
        f"border-top: 1px solid #e2e8f0; color: {_TEXT_MUTED};"
        f"font-size: 13px; line-height: 1.7;"
    )

    title = soup.new_tag("p")
    title["style"] = "margin: 0 0 8px 0; font-weight: 700; color: #4a5568;"
    title.string = "参考资料"
    section.append(title)

    for number, label, href in references:
        item = soup.new_tag("p")
        item["style"] = "margin: 0 0 6px 0; word-break: break-all;"
        item.string = f"[{number}] {label}：{href}"
        section.append(item)

    soup.append(section)
