#!/usr/bin/env python3
"""Regenerate every press/media list on the site from data/media.json.

Usage:  python3 tools/build_media.py          (rewrite files)
        python3 tools/build_media.py --check  (exit 1 if files are out of date)

Each page contains a block delimited by:
    <!-- MEDIA:START -->  ...generated...  <!-- MEDIA:END -->
and, on media.html / media-he.html, also a JSON-LD block in <head>:
    <!-- MEDIA-LD:START -->  ...generated...  <!-- MEDIA-LD:END -->
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
    logo = it.get("logo")
    dims = ""
    if logo and logo.get("width") and logo.get("height"):
        dims = f' width="{logo["width"]}" height="{logo["height"]}"'
    name = it["name"][lang]
    title = it[lang]["title"]
    desc = it[lang]["desc"]
    src = f'<div class="source">{E(it["name"]["en"])}</div>' if show_source else ""
    if logo and logo.get("src"):
        logo_html = (
            f'<img{dims} class="publisher-logo" src="{logo["src"]}" alt="{E(name)}" '
            f'loading="lazy" decoding="async" />'
        )
    else:  # no logo file: show the publisher name as a text wordmark
        logo_html = f'<span class="publisher-name" style="font-weight:800;font-size:20px;letter-spacing:.02em">{E(name)}</span>'
    tag = f'<span class="media-tag">{t["tag"]}</span>' if it.get("sponsored") else ""
    aria_prefix = t["read"].rstrip(":") + ":"
    return (
        f'<article class="{art_cls}"><div>'
        f'<div class="publisher-logo-wrap">{logo_html}</div>'
        f"{src}{tag}<h3>{E(title)}</h3><p>{E(desc)}</p></div>"
        f'<a class="{btn_cls}" href="{E(it["url"])}" target="_blank" rel="noopener noreferrer" '
        f'aria-label="{E(aria_prefix + " " + title)}">{t["read"]}</a></article>'
    )


def build(page, cfg):
    lang, art, btn, src = cfg
    body = "\n".join(card(it, lang, art, btn, src) for it in DATA)
    return f"<!-- MEDIA:START -->\n{body}\n<!-- MEDIA:END -->"


LD_PAGES = {
    "media.html": {
        "lang": "en",
        "url": "https://blueseasonint.com/media.html",
        "name": "Media & Recognition",
        "crumbs": ["Blue Season International", "Media & Recognition"],
        "home": "https://blueseasonint.com/",
    },
    "media-he.html": {
        "lang": "he",
        "url": "https://blueseasonint.com/media-he.html",
        "name": "מדיה ופרסומים",
        "crumbs": ["בלו סיזן אינטרנשיונל", "מדיה ופרסומים"],
        "home": "https://blueseasonint.com/index-he.html",
    },
}


def build_ld(page):
    c = LD_PAGES[page]
    lang = c["lang"]
    graph = [
        {
            "@type": "BreadcrumbList",
            "@id": c["url"] + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": c["crumbs"][0], "item": c["home"]},
                {"@type": "ListItem", "position": 2, "name": c["crumbs"][1], "item": c["url"]},
            ],
        },
        {
            "@type": "CollectionPage",
            "@id": c["url"] + "#webpage",
            "url": c["url"],
            "name": c["name"],
            "inLanguage": lang,
            "about": {"@type": "Person", "name": "Guy Koubbi", "alternateName": "גיא קובי"},
            "isPartOf": {"@type": "WebSite", "url": "https://blueseasonint.com/"},
            "breadcrumb": {"@id": c["url"] + "#breadcrumb"},
            "mainEntity": {
                "@type": "ItemList",
                "numberOfItems": len(DATA),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i + 1,
                        "name": it[lang]["title"],
                        "url": it["url"],
                    }
                    for i, it in enumerate(DATA)
                ],
            },
        },
    ]
    blob = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    blob = blob.replace("</", "<\\/")
    return f'<!-- MEDIA-LD:START -->\n<script type="application/ld+json">\n{blob}\n</script>\n<!-- MEDIA-LD:END -->'


def main():
    check = "--check" in sys.argv
    stale = []
    for page, cfg in PAGES.items():
        p = ROOT / page
        s = p.read_text(encoding="utf-8")
        new, n = re.subn(r"<!-- MEDIA:START -->.*?<!-- MEDIA:END -->", lambda m: build(page, cfg), s, flags=re.S)
        if n != 1:
            sys.exit(f"{page}: expected exactly one MEDIA block, found {n}")
        if page in LD_PAGES:
            new, n2 = re.subn(r"<!-- MEDIA-LD:START -->.*?<!-- MEDIA-LD:END -->", lambda m: build_ld(page), new, flags=re.S)
            if n2 != 1:
                sys.exit(f"{page}: expected exactly one MEDIA-LD block, found {n2}")
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
