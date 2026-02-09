from __future__ import annotations

import difflib
from importlib.util import find_spec
from pathlib import Path

from .fallback_parser import parse_file as parse_file_fallback
from .grammar_parser import parse_file as parse_file_grammar
from .normalize import normalize_verse_text
from .types import ParseError, VerseRecord


def _fmt_ref(book: str, chapter: int, verse: int) -> str:
    return f"{book} {chapter}:{verse}"


def _short(text: str, width: int = 70) -> str:
    value = text.strip()
    if len(value) <= width:
        return value
    return f"{value[: width - 3]}..."


def _has_usfm_grammar() -> bool:
    return find_spec("usfm_grammar") is not None


def _verify_parser_parity(path: Path, grammar_records: list[VerseRecord]) -> None:
    fallback_records = parse_file_fallback(path)
    grammar_map = {(r.book, r.chapter, r.verse): normalize_verse_text(r.text) for r in grammar_records}
    fallback_map = {(r.book, r.chapter, r.verse): normalize_verse_text(r.text) for r in fallback_records}

    mismatches: list[str] = []
    keys_grammar = set(grammar_map)
    keys_fallback = set(fallback_map)

    only_grammar = sorted(keys_grammar - keys_fallback)
    only_fallback = sorted(keys_fallback - keys_grammar)
    for key in only_grammar[:5]:
        mismatches.append(f"missing in fallback: {_fmt_ref(*key)}")
    for key in only_fallback[:5]:
        mismatches.append(f"missing in grammar: {_fmt_ref(*key)}")

    shared = sorted(keys_grammar & keys_fallback)
    sample_size = len(shared) if len(shared) <= 200 else 100
    for key in shared[:sample_size]:
        g = grammar_map[key]
        f = fallback_map[key]
        if g == f:
            continue
        diff = "".join(difflib.ndiff([g], [f]))
        mismatches.append(
            f"text mismatch {_fmt_ref(*key)} | grammar='{_short(g)}' fallback='{_short(f)}' diff='{_short(diff, 110)}'"
        )
        if len(mismatches) >= 5:
            break

    if mismatches:
        joined = "; ".join(mismatches[:5])
        raise ParseError(f"Parser verification failed for {path}: {joined}")


def parse_all(
    usfm_files: list[Path],
    parser: str = "auto",
    *,
    verify_parsers: bool = False,
) -> list[VerseRecord]:
    records: list[VerseRecord] = []
    if parser not in {"auto", "grammar", "fallback"}:
        raise ValueError(f"Unsupported parser mode: {parser}")

    for path in usfm_files:
        if parser == "fallback":
            records.extend(parse_file_fallback(path))
            continue
        if parser == "grammar":
            grammar_records = parse_file_grammar(path)
            if verify_parsers:
                _verify_parser_parity(path, grammar_records)
            records.extend(grammar_records)
            continue
        fallback_records = parse_file_fallback(path)
        if verify_parsers and _has_usfm_grammar():
            grammar_records = parse_file_grammar(path)
            _verify_parser_parity(path, grammar_records)
        records.extend(fallback_records)
    return records
