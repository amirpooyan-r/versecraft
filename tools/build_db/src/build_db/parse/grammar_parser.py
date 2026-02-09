from __future__ import annotations

import re
from pathlib import Path

from ..discover import infer_book_id, normalize_book_id
from .normalize import normalize_verse_text
from .types import ParseError, VerseRecord


_NOTE_MARKERS = {"f", "fe", "ef", "efe", "x", "ex"}
_DIGITS_RE = re.compile(r"(\d+)")


def _extract_digits(value: object) -> int | None:
    if isinstance(value, int):
        return value
    if value is None:
        return None
    match = _DIGITS_RE.search(str(value))
    if not match:
        return None
    return int(match.group(1))


def _extract_book_from_node(node: dict[str, object]) -> str | None:
    marker = str(node.get("marker") or node.get("type") or "").lower()
    if marker not in {"id", "book"}:
        return None
    candidates = [
        node.get("code"),
        node.get("book"),
        node.get("id"),
        node.get("text"),
        node.get("value"),
    ]
    for candidate in candidates:
        normalized = normalize_book_id(str(candidate or ""))
        if normalized:
            return normalized
    return None


def _extract_chapter_from_node(node: dict[str, object]) -> int | None:
    marker = str(node.get("marker") or node.get("type") or "").lower()
    if marker != "c" and "chapter" not in marker:
        return None
    for key in ("number", "chapter", "sid", "value"):
        chapter = _extract_digits(node.get(key))
        if chapter is not None:
            return chapter
    return None


def _extract_verse_from_node(node: dict[str, object]) -> int | None:
    marker = str(node.get("marker") or node.get("type") or "").lower()
    if marker != "v" and "verse" not in marker:
        return None
    for key in ("number", "verse", "sid", "value"):
        verse = _extract_digits(node.get(key))
        if verse is not None:
            return verse
    return None


def _is_note_node(node: dict[str, object]) -> bool:
    marker = str(node.get("marker") or node.get("type") or "").lower()
    return marker in _NOTE_MARKERS


def _to_usj(path: Path, text: str) -> object:
    try:
        import usfm_grammar
    except Exception as exc:  # pragma: no cover - environment dependent
        raise ParseError(
            "usfm-grammar not available (install extras or use --parser fallback)"
        ) from exc

    parser_cls = getattr(usfm_grammar, "USFMParser", None)
    if parser_cls is None:
        raise ParseError("usfm-grammar API missing USFMParser")

    parser = parser_cls(text)
    to_usj = getattr(parser, "to_usj", None)
    if to_usj is None:
        raise ParseError("usfm-grammar API does not expose to_usj()")

    attempts: list[dict[str, object]] = [
        {},
        {"combine_texts": False, "ignore_errors": False},
    ]
    filter_cls = getattr(usfm_grammar, "Filter", None)
    if filter_cls is not None and all(
        hasattr(filter_cls, name) for name in ("BCV", "TEXT", "NOTES")
    ):
        attempts.insert(
            0,
            {
                "include_markers": filter_cls.BCV + filter_cls.TEXT,
                "exclude_markers": filter_cls.NOTES,
                "combine_texts": False,
                "ignore_errors": False,
            },
        )

    last_type_error: TypeError | None = None
    for kwargs in attempts:
        try:
            usj = to_usj(**kwargs)
            if usj is None:
                raise ParseError(f"usfm-grammar returned empty parse result for {path}")
            return usj
        except TypeError as exc:
            last_type_error = exc
            continue
        except ParseError:
            raise
        except Exception as exc:  # pragma: no cover - dependency behavior
            raise ParseError(f"usfm-grammar parse failed for {path}: {exc}") from exc

    if last_type_error is not None:
        raise ParseError(f"usfm-grammar to_usj API mismatch: {last_type_error}") from last_type_error
    raise ParseError(f"usfm-grammar parse failed for {path}")


def _extract_records(path: Path, usj: object, inferred_book: str | None) -> list[VerseRecord]:
    book = inferred_book
    chapter: int | None = None
    verse: int | None = None
    buffer: list[str] = []
    records: list[VerseRecord] = []

    def flush() -> None:
        nonlocal buffer, verse
        if chapter is None or verse is None or not book:
            buffer = []
            verse = None
            return
        normalized = normalize_verse_text(" ".join(buffer))
        if normalized:
            key = (book, chapter, verse)
            if records and (records[-1].book, records[-1].chapter, records[-1].verse) == key:
                previous = records.pop()
                merged = normalize_verse_text(f"{previous.text} {normalized}")
                if merged:
                    records.append(
                        VerseRecord(
                            book=previous.book,
                            chapter=previous.chapter,
                            verse=previous.verse,
                            text=merged,
                        )
                    )
            else:
                records.append(VerseRecord(book=book, chapter=chapter, verse=verse, text=normalized))
        buffer = []
        verse = None

    def walk(node: object) -> None:
        nonlocal book, chapter, verse
        if isinstance(node, str):
            if verse is not None:
                buffer.append(node)
            return
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if not isinstance(node, dict):
            return

        maybe_book = _extract_book_from_node(node)
        if maybe_book:
            book = maybe_book

        if _is_note_node(node):
            return

        maybe_chapter = _extract_chapter_from_node(node)
        if maybe_chapter is not None:
            flush()
            chapter = maybe_chapter

        maybe_verse = _extract_verse_from_node(node)
        if maybe_verse is not None:
            if chapter is None:
                raise ParseError(f"Verse before chapter marker in {path}")
            flush()
            verse = maybe_verse

        for key in ("text", "value"):
            value = node.get(key)
            if isinstance(value, str) and verse is not None:
                buffer.append(value)

        for key in ("content", "children"):
            children = node.get(key)
            if children is not None:
                walk(children)

    walk(usj)
    flush()

    if not book:
        raise ParseError(f"Unable to infer canonical book id for {path}")
    if not records:
        raise ParseError(f"No verse records parsed from {path}")
    return records


def parse_file(path: Path) -> list[VerseRecord]:
    text = path.read_text(encoding="utf-8", errors="replace")
    usj = _to_usj(path, text)
    inferred = infer_book_id(path, text)
    return _extract_records(path, usj, inferred)
