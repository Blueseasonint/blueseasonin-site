#!/usr/bin/env python3
"""Keep <lastmod> in sitemap.xml equal to the date of the last commit that touched each page.

Usage:  python3 tools/build_sitemap.py          (rewrite sitemap.xml)
        python3 tools/build_sitemap.py --check  (exit 1 if out of date)

Needs full git history (the GitHub Action checks out with fetch-depth: 0).
In a shallow clone the dates would be wrong, so the script refuses to run there.
Only <lastmod> is touched; everything else (hreflang links, video entries) is hand-maintained.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"
BASE = "https://blueseasonint.com/"


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout.strip()


def main():
    if git("rev-parse", "--is-shallow-repository") == "true":
        sys.exit("shallow clone: run `git fetch --unshallow` first (dates would be wrong)")
    text = SITEMAP.read_text(encoding="utf-8")

    def fix(m):
        block = m.group(0)
        loc = re.search(r"<loc>([^<]+)</loc>", block).group(1)
        rel = loc[len(BASE):] or "index.html"
        if not (ROOT / rel).exists():
            return block
        date = git("log", "-1", "--format=%cs", "--", rel)
        if not date:
            return block
        return re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{date}</lastmod>", block)

    new = re.sub(r"<url>.*?</url>", fix, text, flags=re.S)
    if new == text:
        print("sitemap already up to date")
        return
    if "--check" in sys.argv:
        print("sitemap.xml is out of date")
        sys.exit(1)
    SITEMAP.write_text(new, encoding="utf-8")
    print("sitemap.xml updated")


main()
