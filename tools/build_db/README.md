# VerseCraft — SQLite Build Tool (dev-only)

This folder contains VerseCraft’s **developer tooling** for building the SQLite
Bible databases used by the Flutter app.

VerseCraft ships Bible text **offline** inside SQLite files (**one DB per translation**).
These databases are built **at build time** (by developers / CI), not at runtime
inside the Flutter app.

> ✅ Dev-only: This tool is **not** used by the Flutter runtime and does not add
> any Python dependencies to the mobile app.

---

## What this tool does

This tool builds a VerseCraft translation database from **USFM** sources:

**USFM → parse → normalize → validate → SQLite → sanity-check**

Why USFM?
- **USFM (Unified Standard Format Markers)** is a widely used plain-text Bible markup format.
- Most Bible translations publish USFM sources; it’s a good “source of truth” format.

---

## What is USFM?

USFM files are plain-text with markers describing structure.

Common markers:
- `\id`  — Book identifier
- `\c`   — Chapter number
- `\v`   — Verse number
- `\p`   — Paragraph
- `\q1`… — Poetry line levels
- `\f ... \f*` — Footnotes (should be stripped from final verse text)

Our pipeline converts USFM into a simple verse table:
`(book_id, chapter, verse, text)`.

---

## Requirements

- **Python 3.12+**
- Run in a local virtual environment (**venv**) for isolation.
- Dependencies are pinned in `requirements.txt` for reproducible builds.
- Primary v1 parser is the built-in **fallback parser**.
- `usfm-grammar` is optional for verification and grammar-only runs.
- On Windows, fallback mode works without native build tools.
- Installing `usfm-grammar` may require C/C++ build tooling (for example MSVC on Windows).

---

## Virtual environment (recommended)

The `.venv/` folder must NOT be committed.

### Windows (PowerShell)

1) Create & activate venv
- cd tools/build_db
- python -m venv .venv
- .\.venv\Scripts\activate

2) Install pinned dependencies
- pip install -r requirements.txt
- pip install -e .

### macOS / Linux

1) Create & activate venv
- cd tools/build_db
- python3 -m venv .venv
- source .venv/bin/activate

2) Install pinned dependencies
- pip install -r requirements.txt
- pip install -e .

3) Verify CLI wiring
- build-db --help
- python -m build_db --help

---

## VerseCraft SQLite schema

Tables:
- `verses(book TEXT, chapter INTEGER, verse INTEGER, text TEXT, PRIMARY KEY(book,chapter,verse))`
- `meta(key TEXT PRIMARY KEY, value TEXT)`

Notes:
- `book` is a canonical book ID (e.g. `gen`, `jhn`, `psa`), not a localized name.
- Localized book names belong in the Flutter UI localization files, not the DB.

---

## Inputs

The tool accepts either:
1) A local directory containing USFM/SFM files (e.g., `44JHN...SFM`, `01GEN...USFM`, etc.)
2) A local `.zip` file containing USFM/SFM sources
3) A URL to a `.zip` file containing USFM/SFM sources

For zip inputs, the tool should download (if URL), extract to a local cache folder, then parse.

Parser modes:
- `--parser fallback` uses fallback parser only.
- `--parser grammar` uses `usfm-grammar` only. If unavailable or parsing fails, build fails.
- `--parser auto` is the default and uses fallback parser output.
- In `auto`, `--verify-parsers` runs grammar comparison when `usfm-grammar` is available.
- `--verify-parsers` compares grammar output vs fallback output and fails on mismatch.

Recommended local folders (ignored by git):
- `tools/build_db/sources/` (place USFM zips or extracted folders here)
- `tools/build_db/out/` (generated SQLite DBs)
- `tools/build_db/.cache/` (download/extract cache)

---

## Output

A single SQLite file for one translation, for example:
- `tools/build_db/out/bsb.sqlite`

This file can then be copied into the Flutter app assets as:
- `assets/bibles/bsb.sqlite`

(Exact app asset workflow may vary by build step.)

---

## Sanity-check (after build)

After building a real translation DB, we run a quick sanity-check such as:
- Query: `jhn 3:16–18`
- Expected:
  - 3 rows returned (verses 16, 17, 18)
  - non-empty text for each verse

If sanity-check fails, the build should exit with a non-zero code.

---

## Recommended v1 workflow

1) Install deps in `tools/build_db`:
- `pip install -r requirements.txt`
- `pip install -e .`

2) Build using fallback output (portable default):
- `build-db --input <usfm_dir_or_zip> --out <sqlite_path> --translation-id <id> --translation-name <name> --parser auto --verify-parsers`

3) For release prep, run verification in an environment with grammar dependencies available (Linux/WSL recommended):
- `build-db --input <usfm_dir_or_zip> --out <sqlite_path> --translation-id <id> --translation-name <name> --parser auto --verify-parsers`

Treat parser mismatches as blockers before publishing assets.

---

## Future subcommands (tool roadmap)

As VerseCraft grows, this dev tool can evolve into a small “Bible DB toolkit”, for example:
- `build` — Build DB from USFM sources
- `validate-db` — Check schema + verse coverage + meta fields
- `sanity-check` — Run quick verse queries after build
- `db-stats` — Print counts per book, chapters, verses, etc.
- `export-range` — Export a small verse range to JSON/text for debugging

These remain **dev-only** and never ship with the Flutter runtime.
