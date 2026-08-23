#!/usr/bin/env python3
"""Render Chirpy header cards from tools/header-cards.json + post front matter."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "_posts"
OUT = ROOT / "assets" / "img" / "headers"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
PREVIEW = "http://127.0.0.1:8765/header-card-preview.html"
TYPES = {
    "howto": "手順",
    "think": "思考",
    "fail": "失敗ログ",
    "recap": "ふりかえり",
    "extra": "番外編",
}


def parse_front_matter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match:
        raise ValueError("front matter missing")
    data: dict[str, str] = {}
    for raw_key in ("title", "description"):
        found = re.search(
            rf"^{raw_key}:\s*(?:\"([^\"]*)\"|'([^']*)'|(.*))$",
            match.group(1),
            re.M,
        )
        if found:
            data[raw_key] = (found.group(1) or found.group(2) or found.group(3) or "").strip()
    return data


def upsert_image(text: str, rel_path: str, alt: str) -> str:
    block = f"image:\n  path: {rel_path}\n  alt: {json.dumps(alt, ensure_ascii=False)}"
    if re.search(r"^image:\s*$", text, re.M):
        return re.sub(
            r"^image:\n(?:  .+\n)+",
            block + "\n",
            text,
            count=1,
            flags=re.M,
        )
    if re.search(r"^image:\s+\S+", text, re.M):
        return re.sub(r"^image:\s+\S+\s*$", block, text, count=1, flags=re.M)
    return re.sub(r"\n---[ \t]*\r?\n", f"\n{block}\n---\n", text, count=1)


def render(slug: str, card: str, title: str, desc: str) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f"{slug}.png"
    query = urllib.parse.urlencode(
        {
            "card": card,
            "title": title,
            "desc": desc,
            "long": "1" if len(title) > 28 else "0",
        },
        quote_via=urllib.parse.quote,
    )
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--virtual-time-budget=4000",
        "--window-size=1200,630",
        f"--screenshot={dest}",
        f"{PREVIEW}?{query}",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return dest


def main() -> int:
    mapping = json.loads((ROOT / "tools" / "header-cards.json").read_text())
    write_front = "--no-front-matter" not in sys.argv
    for slug, card in mapping.items():
        post = POSTS / f"{slug}.md"
        meta = parse_front_matter(post.read_text())
        title = meta.get("title")
        desc = meta.get("description")
        if not title or not desc:
            raise SystemExit(f"{slug}: title/description が必要です")
        dest = OUT / f"{slug}.png"
        if dest.exists() and "--force" not in sys.argv:
            print(f"{TYPES[card]}\tskip {dest.name}")
        else:
            dest = render(slug, card, title, desc)
            print(f"{TYPES[card]}\t{dest.name}")
        if write_front:
            rel = f"/assets/img/headers/{slug}.png"
            post.write_text(upsert_image(post.read_text(), rel, title))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
