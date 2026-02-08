from __future__ import annotations

import re
from pathlib import Path

from ..discover import infer_book_id
from .normalize import normalize_verse_text
from .types import ParseError, VerseRecord

_CHAPTER_RE = re.compile(r"^\\c\s+(\d+)\b")
_VERSE_RE = re.compile(r"^\\v\s+(\d+)(?:[a-z]?|-\d+)?\s*(.*)$")
_MARKER_WITH_TEXT_RE = re.compile(r"^\\[A-Za-z0-9][A-Za-z0-9-]*\*?\s*(.*)$")


def parse_file(path: Path) -> list[VerseRecord]:
    text = path.read_text(encoding="utf-8", errors="replace")
    book = infer_book_id(path, text)
    if not book:
        raise ParseError(f"Unable to infer canonical book id for {path}")

    records: list[VerseRecord] = []
    chapter: int | None = None
    verse: int | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal verse, buffer
        if chapter is None or verse is None:
            buffer = []
            return
        normalized = normalize_verse_text(" ".join(buffer))
        if normalized:
            records.append(VerseRecord(book=book, chapter=chapter, verse=verse, text=normalized))
        verse = None
        buffer = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("\\id "):
            maybe = infer_book_id(path, line)
            if maybe:
                book = maybe
            continue
        chapter_match = _CHAPTER_RE.match(line)
        if chapter_match:
            flush()
            chapter = int(chapter_match.group(1))
            continue
        verse_match = _VERSE_RE.match(line)
        if verse_match:
            flush()
            verse = int(verse_match.group(1))
            payload = verse_match.group(2).strip()
            if payload:
                buffer.append(payload)
            continue
        if verse is None:
            continue
        if line.startswith("\\"):
            marker_payload = _MARKER_WITH_TEXT_RE.match(line)
            if marker_payload:
                payload = marker_payload.group(1).strip()
                if payload:
                    buffer.append(payload)
            continue
        buffer.append(line)

    flush()
    if not records:
        raise ParseError(f"No verse records parsed from {path}")
    return records
