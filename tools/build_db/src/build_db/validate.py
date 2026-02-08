from __future__ import annotations

from .parse.types import VerseRecord


def validate_records(records: list[VerseRecord]) -> None:
    if not records:
        raise ValueError("No verses extracted from input")
    seen: set[tuple[str, int, int]] = set()
    for record in records:
        if len(record.book) != 3 or record.book != record.book.lower():
            raise ValueError(f"Invalid canonical book id: {record.book}")
        if record.chapter <= 0:
            raise ValueError(f"Invalid chapter for {record.book}: {record.chapter}")
        if record.verse <= 0:
            raise ValueError(f"Invalid verse for {record.book} {record.chapter}: {record.verse}")
        if not record.text.strip():
            raise ValueError(f"Blank verse text for {record.book} {record.chapter}:{record.verse}")
        key = (record.book, record.chapter, record.verse)
        if key in seen:
            raise ValueError(f"Duplicate verse reference: {record.book} {record.chapter}:{record.verse}")
        seen.add(key)
