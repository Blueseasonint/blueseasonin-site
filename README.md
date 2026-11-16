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
   The homepages show only the first 6 items (`HOME_LIMIT` in `tools/build_media.py`) and link to
   the full media page, so put the publications you most want on the homepage first.
   Logo size is computed from the logo's `width`/`height`, so always fill both in.
2. Commit. The GitHub Action "Rebuild media lists" regenerates the four pages
   and commits them automatically.
3. Or run locally: `python3 tools/build_media.py` (`--check` to verify sync).
4. Put new logos in `assets/media/`.
