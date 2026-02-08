from __future__ import annotations

import re
import sqlite3
from pathlib import Path

_SANITY_RE = re.compile(r"^\s*([a-z0-9]{3})\s+(\d+):(\d+)(?:-(\d+))?\s*$", re.IGNORECASE)


def _parse_sanity(spec: str) -> tuple[str, int, list[int]]:
    match = _SANITY_RE.match(spec)
    if not match:
        raise ValueError(f"Invalid sanity check spec: {spec}")
    book = match.group(1).lower()
    chapter = int(match.group(2))
    start = int(match.group(3))
    end = int(match.group(4) or start)
    if start <= 0 or end < start:
        raise ValueError(f"Invalid sanity verse range: {spec}")
    return book, chapter, list(range(start, end + 1))


def run_sanity_check(db_path: Path, spec: str = "jhn 3:16-18") -> None:
    book, chapter, verses = _parse_sanity(spec)
    placeholders = ",".join("?" for _ in verses)
    query = (
        f"SELECT verse, text FROM verses WHERE book=? AND chapter=? AND verse IN ({placeholders}) "
        "ORDER BY verse"
    )
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(query, [book, chapter, *verses]).fetchall()
    if len(rows) != len(verses):
        raise ValueError(
            f"Sanity check failed for {spec}: expected {len(verses)} verses, got {len(rows)}"
        )
    missing = [verse for verse, text in rows if not str(text).strip()]
    if missing:
        raise ValueError(f"Sanity check failed for {spec}: blank text in verses {missing}")
