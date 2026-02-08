from __future__ import annotations

import sqlite3
from pathlib import Path

from .parse.types import VerseRecord


def write_sqlite(out_path: Path, records: list[VerseRecord], meta: dict[str, str]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        out_path.unlink()

    with sqlite3.connect(out_path) as conn:
        conn.execute(
            "CREATE TABLE verses("
            "book TEXT, chapter INTEGER, verse INTEGER, text TEXT, "
            "PRIMARY KEY(book,chapter,verse))"
        )
        conn.execute("CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT)")
        conn.executemany(
            "INSERT INTO verses(book, chapter, verse, text) VALUES(?, ?, ?, ?)",
            [(r.book, r.chapter, r.verse, r.text) for r in records],
        )
        conn.executemany(
            "INSERT INTO meta(key, value) VALUES(?, ?)",
            sorted(meta.items(), key=lambda item: item[0]),
        )
        conn.commit()
