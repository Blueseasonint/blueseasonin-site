# blueseasonin-site

Static site for blueseasonint.com (GitHub Pages).

## Press / media list — single source

All press items live in **`data/media.json`**. The lists on these four pages are
generated from it and must not be edited by hand (between the
`<!-- MEDIA:START -->` / `<!-- MEDIA:END -->` markers):

- `index.html`, `index-he.html` (homepage "Media" section)
- `media.html`, `media-he.html` (full media pages)

### Add or change a publication

1. Edit `data/media.json`. Each item has: `url`, `sponsored` (true/false),
   `logo` (`src`, `width`, `height`), `name` (`he` / `en`), and `he` / `en`
   `title` + `desc`. List order = display order (same on every page).
2. Commit. The GitHub Action "Rebuild media lists" regenerates the four pages
   and commits them automatically.
3. Or run locally: `python3 tools/build_media.py` (`--check` to verify sync).
4. Put new logos in `assets/media/`.
