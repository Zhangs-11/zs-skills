#!/usr/bin/env python3
"""
make_subtitles.py — 从口播念稿 + 配音音频，生成 .srt 字幕文件。

按每句字数占比把音频总时长切成若干段（朗读时长大体正比于字数），
生成可直接导入剪映/Pr 的 .srt。无需逐句对齐标注。

用法：
  python3 make_subtitles.py \
    --voice-txt ~/公众号草稿/分发/<文章>/voice.txt \
    --audio     ~/公众号草稿/分发/<文章>/voice.m4a \
    --out       ~/公众号草稿/分发/<文章>/subtitles.srt

时长获取优先 afinfo(macOS)，回退 ffprobe，再回退按字数估算(每字约 0.22s)。
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path


def audio_duration(audio: Path) -> float:
    # macOS afinfo
    try:
        out = subprocess.run(["afinfo", str(audio)], capture_output=True, text=True).stdout
        m = re.search(r"estimated duration:\s*([\d.]+)\s*sec", out)
        if m:
            return float(m.group(1))
    except FileNotFoundError:
        pass
    # ffprobe
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(audio)],
            capture_output=True, text=True,
        ).stdout.strip()
        if out:
            return float(out)
    except FileNotFoundError:
        pass
    return 0.0


def fmt_ts(sec: float) -> str:
    if sec < 0:
        sec = 0
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms == 1000:
        ms = 0
        s += 1
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def char_len(line: str) -> int:
    # 用于配时的“朗读重量”：忽略空白，标点也算一点停顿
    return max(1, len(re.sub(r"\s", "", line)))


def build_srt(lines: list[str], duration: float) -> str:
    weights = [char_len(l) for l in lines]
    total = sum(weights)
    if duration <= 0:
        duration = total * 0.22  # 回退估算
    blocks = []
    acc = 0.0
    for i, (line, w) in enumerate(zip(lines, weights), start=1):
        start = acc
        acc += duration * w / total
        end = acc
        blocks.append(f"{i}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{line}\n")
    return "\n".join(blocks)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice-txt", required=True, type=Path)
    ap.add_argument("--audio", type=Path, default=None)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    lines = [l.strip() for l in args.voice_txt.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        print("ERROR: voice.txt 为空", file=sys.stderr)
        return 1

    duration = audio_duration(args.audio) if args.audio else 0.0
    srt = build_srt(lines, duration)
    args.out.write_text(srt, encoding="utf-8")
    print(f"SUCCESS: 写入 {args.out}（{len(lines)} 句, 时长 {duration:.1f}s）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
