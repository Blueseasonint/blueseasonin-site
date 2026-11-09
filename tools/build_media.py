#!/usr/bin/env python3
"""Regenerate every press/media list on the site from data/media.json.

Usage:  python3 tools/build_media.py          (rewrite files)
        python3 tools/build_media.py --check  (exit 1 if files are out of date)

Each page contains a block delimited by:
    <!-- MEDIA:START -->  ...generated...  <!-- MEDIA:END -->
Never edit inside those markers by hand; edit data/media.json instead.
"""
import json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "media.json").read_text(encoding="utf-8"))["items"]
E = lambda s: html.escape(s, quote=True)

LANG = {
    "he": {"tag": "תוכן שיווקי", "read": "לקריאת הכתבה"},
    "en": {"tag": "Sponsored content", "read": "Read Article"},
}

# page -> (lang, article class, button class, show publisher-name line)
PAGES = {
    "index-he.html": ("he", "media-card", "btn", False),
    "index.html": ("en", "media-card", "btn", False),
    "media-he.html": ("he", "press-card", "btn btn-primary", False),
    "media.html": ("en", "media-card", "button", True),
}


def card(it, lang, art_cls, btn_cls, show_source):
    t = LANG[lang]
    logo = it["logo"]
    dims = ""
    if logo.get("width") and logo.get("height"):
        dims = f' width="{logo["width"]}" height="{logo["height"]}"'
    name = it["name"][lang]
    title = it[lang]["title"]
    desc = it[lang]["desc"]
    src = f'<div class="source">{E(it["name"]["en"])}</div>' if show_source else ""
    tag = f'<span class="media-tag">{t["tag"]}</span>' if it.get("sponsored") else ""
    aria_prefix = t["read"].rstrip(":") + ":"
    return (
        f'<article class="{art_cls}"><div>'
        f'<div class="publisher-logo-wrap"><img{dims} class="publisher-logo" '
        f'src="{logo["src"]}" alt="{E(name)}" loading="lazy" decoding="async" /></div>'
        f"{src}{tag}<h3>{E(title)}</h3><p>{E(desc)}</p></div>"
        f'<a class="{btn_cls}" href="{E(it["url"])}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{E(aria_prefix + " " + title)}">{t["read"]}</a></article>'
    )


def build(page, cfg):
    lang, art, btn, src = cfg
    body = "\n".join(card(it, lang, art, btn, src) for it in DATA)
    return f"<!-- MEDIA:START -->\n{body}\n<!-- MEDIA:END -->"


def main():
    check = "--check" in sys.argv
    stale = []
    for page, cfg in PAGES.items():
        p = ROOT / page
        s = p.read_text(encoding="utf-8")
        new, n = re.subn(r"<!-- MEDIA:START -->.*?<!-- MEDIA:END -->", lambda m: build(page, cfg), s, flags=re.S)
        if n != 1:
            sys.exit(f"{page}: expected exactly one MEDIA block, found {n}")
        if new != s:
            stale.append(page)
            if not check:
                p.write_text(new, encoding="utf-8")
    if check and stale:
        print("Out of date:", ", ".join(stale))
        sys.exit(1)
    print(("Would update: " if check else "Updated: ") + (", ".join(stale) or "nothing (already in sync)"))


if __name__ == "__main__":
    main()
