#!/usr/bin/env python3
"""AI HOT 选题助手 - 获取今日热点，格式化为选题表"""

import json
import os
import re
import sys
import glob
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
BASE = "https://aihot.virxact.com"
DRAFTS_DIR = Path.home() / "公众号草稿"


def fetch_daily():
    req = Request(f"{BASE}/api/public/daily", headers={"User-Agent": UA})
    with urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fetch_items(hours=24, take=30, mode="selected"):
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    url = f"{BASE}/api/public/items?mode={mode}&since={since}&take={take}"
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    return data.get("items", [])


def fetch_merged(hours=24):
    """selected 精选通道为主，all 全量通道兜底补漏。

    精选通道可能漏掉重大新闻（如 Kimi K3 发布当天全量通道有 24 条、
    精选只收录 1 条且时间戳错误），所以把全量通道里的高分条目也并进来，
    靠 dedup 收敛同话题的重复报道。
    """
    selected = fetch_items(hours=hours, take=50, mode="selected")
    seen_urls = {it.get("url") for it in selected}
    try:
        extra = fetch_items(hours=hours, take=100, mode="all")
    except Exception:
        extra = []
    for it in extra:
        if it.get("score", 0) >= 55 and it.get("url") not in seen_urls:
            selected.append(it)
            seen_urls.add(it.get("url"))
    return selected


def get_recent_draft_titles(days=7):
    titles = []
    if not DRAFTS_DIR.exists():
        return titles
    cutoff = datetime.now().timestamp() - days * 86400
    for f in DRAFTS_DIR.glob("*.md"):
        if f.stat().st_mtime < cutoff:
            continue
        titles.append(f.stem.replace("-", " ").replace("_", " "))
    return titles


def extract_source_info(source_name):
    x_match = re.search(r'X[：:]\s*(.+?)\s*\(@(\w+)\)', source_name)
    if x_match:
        return f"𝕏 @{x_match.group(2)}", "X"
    if source_name.startswith("X：") or source_name.startswith("X:"):
        name = re.split(r'[：:]', source_name, maxsplit=1)[-1].strip()
        return f"𝕏 {name[:15]}", "X"
    wx_match = re.search(r'公众号[：:]\s*(.+?)(?:[（(]|$)', source_name)
    if wx_match:
        return wx_match.group(1).strip()[:12], "公众号"
    if "Hacker News" in source_name:
        return "HN", "HN"
    if "IT之家" in source_name:
        return "IT之家", "资讯"
    clean = re.split(r'[（(]', source_name)[0].strip()
    return clean[:15], "其他"


def time_ago(published_at):
    try:
        pub = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        hours = (now - pub).total_seconds() / 3600
        if hours < 1:
            return f"~{max(1, int(hours * 60))}m"
        if hours < 24:
            return f"~{hours:.1f}h"
        return f"~{hours / 24:.0f}d"
    except Exception:
        return "?"


def main():
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    try:
        raw_items = fetch_merged(hours=24)
    except (URLError, Exception) as e:
        json.dump({"error": f"AI HOT API 不可用: {e}"}, sys.stdout, ensure_ascii=False)
        sys.exit(1)

    now_str = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    CATEGORY_MAP = {
        "ai-models": "模型",
        "ai-products": "产品",
        "industry": "行业",
        "paper": "论文",
        "tip": "观点",
    }

    all_items = []
    for item in raw_items:
        source_display, source_type = extract_source_info(item.get("source", ""))
        raw_time = item.get("publishedAt", "")
        try:
            pub_dt = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
            pub_bj = (pub_dt + timedelta(hours=8)).strftime("%m-%d %H:%M")
        except Exception:
            pub_bj = ""
        all_items.append({
            "title": item["title"],
            "source": source_display,
            "source_type": source_type,
            "time_ago": time_ago(raw_time),
            "published": pub_bj,
            "category": CATEGORY_MAP.get(item.get("category", ""), "其他"),
            "score": item.get("score", 0),
            "summary": item.get("summary", ""),
            "url": item.get("url", ""),
        })

    all_items.sort(key=lambda x: x["score"], reverse=True)

    def dedup_key(title):
        clean = re.sub(r'[^\w]', '', title.lower())
        keywords = set(re.findall(r'[一-鿿]+|[a-z]{3,}', clean))
        return frozenset(keywords)

    LATIN_STOPWORDS = {"ai", "llm", "app", "api", "the", "and", "for", "with"}

    def entity_tokens(title):
        # 拉丁实体词（kimi、k3、grok、fable 等），同话题的不同报道靠它们收敛
        tokens = set(re.findall(r'[a-z]+\d+[a-z0-9]*|\d*[a-z]{2,}', title.lower()))
        return tokens - LATIN_STOPWORDS

    seen_groups = []
    unique = []
    for item in all_items:
        keys = dedup_key(item["title"])
        ents = entity_tokens(item["title"])
        is_dup = False
        for seen_keys, seen_ents in seen_groups:
            overlap = len(keys & seen_keys) / max(len(keys | seen_keys), 1)
            if overlap > 0.3 or len(ents & seen_ents) >= 2:
                is_dup = True
                break
        if not is_dup:
            seen_groups.append((keys, ents))
            unique.append(item)

    recent_drafts = get_recent_draft_titles()
    items = unique[:top_n]
    for i, item in enumerate(items):
        item["rank"] = i + 1

    output = {
        "date": today,
        "fetched_at": now_str,
        "total": len(unique),
        "showing": len(items),
        "recent_drafts": recent_drafts,
        "items": items,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
