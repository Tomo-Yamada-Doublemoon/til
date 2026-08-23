#!/usr/bin/env python3
"""Render Chirpy header cards from tools/header-cards.json + post front matter."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
POSTS = ROOT / "_posts"
OUT = ROOT / "assets" / "img" / "headers"
JSON_PATH = TOOLS / "header-cards.json"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
PREVIEW_HOST = "127.0.0.1:8765"
PREVIEW = f"http://{PREVIEW_HOST}/header-card-preview.html"
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


def preview_server_alive() -> bool:
    try:
        urllib.request.urlopen(PREVIEW, timeout=1)
        return True
    except (urllib.error.URLError, OSError):
        return False


def ensure_preview_server() -> subprocess.Popen | None:
    """Start the tools/ preview server if it isn't already up. Returns the
    process we started (caller must stop it), or None if one was already running."""
    if preview_server_alive():
        return None
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8765", "--directory", str(TOOLS)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        if preview_server_alive():
            return proc
        time.sleep(0.1)
    proc.terminate()
    raise SystemExit(f"preview server did not come up on {PREVIEW_HOST}")


def load_mapping() -> dict[str, str]:
    if JSON_PATH.exists():
        return json.loads(JSON_PATH.read_text())
    return {}


def save_mapping(mapping: dict[str, str]) -> None:
    JSON_PATH.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n")


def render_one(slug: str, card: str, write_front: bool, force: bool) -> None:
    post = POSTS / f"{slug}.md"
    if not post.exists():
        raise SystemExit(f"{slug}: _posts/{slug}.md が見つかりません")
    meta = parse_front_matter(post.read_text())
    title = meta.get("title")
    desc = meta.get("description")
    if not title or not desc:
        raise SystemExit(f"{slug}: title/description が必要です")
    dest = OUT / f"{slug}.png"
    if dest.exists() and not force:
        print(f"{TYPES[card]}\tskip {dest.name}")
    else:
        dest = render(slug, card, title, desc)
        print(f"{TYPES[card]}\t{dest.name}")
    if write_front:
        rel = f"/assets/img/headers/{slug}.png"
        post.write_text(upsert_image(post.read_text(), rel, title))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", help="この1本だけ処理する（例: 2026-08-23-example）")
    parser.add_argument("--card", choices=sorted(TYPES), help="カードタイプ。未登録slugならJSONへ追加、既存ならJSONを上書き")
    parser.add_argument("--force", action="store_true", help="既存PNGがあっても再生成する")
    parser.add_argument("--no-front-matter", action="store_true", help="front matterのimage:を書き換えない")
    args = parser.parse_args()

    write_front = not args.no_front_matter
    mapping = load_mapping()

    started_server = ensure_preview_server()
    try:
        if args.slug:
            if args.card:
                if mapping.get(args.slug) != args.card:
                    mapping[args.slug] = args.card
                    save_mapping(mapping)
            elif args.slug not in mapping:
                raise SystemExit(f"{args.slug}: header-cards.json未登録です。--card <type> を指定してください")
            render_one(args.slug, mapping[args.slug], write_front, args.force)
        else:
            for slug, card in mapping.items():
                render_one(slug, card, write_front, args.force)
    finally:
        if started_server is not None:
            started_server.terminate()
            started_server.wait()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
