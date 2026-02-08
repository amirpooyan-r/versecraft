from __future__ import annotations

from pathlib import Path

from .fallback_parser import parse_file as parse_file_fallback
from .grammar_parser import parse_file as parse_file_grammar
from .types import ParseError, VerseRecord


def parse_all(usfm_files: list[Path], parser: str = "auto") -> list[VerseRecord]:
    records: list[VerseRecord] = []
    if parser not in {"auto", "grammar", "fallback"}:
        raise ValueError(f"Unsupported parser mode: {parser}")

    for path in usfm_files:
        if parser == "fallback":
            records.extend(parse_file_fallback(path))
            continue
        if parser == "grammar":
            records.extend(parse_file_grammar(path))
            continue
        try:
            records.extend(parse_file_grammar(path))
        except (ParseError, NotImplementedError):
            records.extend(parse_file_fallback(path))
    return records
