VerseCraft SQLite Build Tool

This dev-only tool builds a SQLite Bible database with the VerseCraft schema.

Schema
- verses(book TEXT, chapter INTEGER, verse INTEGER, text TEXT, PRIMARY KEY(book,chapter,verse))
- meta(key TEXT PRIMARY KEY, value TEXT)

Input format
The script expects a JSON file with this shape:
{
  "translationId": "bsb",
  "verses": [
    {"book": "jhn", "chapter": 3, "verse": 16, "text": "..."}
  ],
  "meta": {
    "name": "Example Name",
    "lang": "en",
    "direction": "ltr",
    "license": "Example License",
    "source": "Example Source"
  }
}

Notes
- meta is optional; if missing, meta fields are inserted with empty strings.
- book should be a stable identifier (e.g., "jhn").

Usage
Run from the repo root:
python tools/build_db/build_sqlite.py --input tools/build_db/sample_bsb_min.json --output build/bsb.sqlite
