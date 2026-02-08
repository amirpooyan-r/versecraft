from __future__ import annotations

from pathlib import Path

from .types import ParseError, VerseRecord


def parse_file(path: Path) -> list[VerseRecord]:
    try:
        from usfm_grammar import Filter, USFMParser
    except Exception as exc:  # pragma: no cover - environment dependent
        raise ParseError("usfm-grammar not available") from exc

    text = path.read_text(encoding="utf-8", errors="replace")
    parser = USFMParser(text)
    if not hasattr(parser, "to_usj"):
        raise NotImplementedError("usfm-grammar integration unverified for this API")

    try:
        usj = parser.to_usj(
            include_markers=Filter.BCV + Filter.TEXT,
            exclude_markers=Filter.NOTES,
            combine_texts=False,
            ignore_errors=True,
        )
    except Exception as exc:  # pragma: no cover - dependency behavior
        raise ParseError(f"usfm-grammar parse failed for {path}") from exc

    # Parsing USJ structures is intentionally deferred unless tested against known API.
    raise NotImplementedError(
        "usfm-grammar produced USJ output, but extraction is unverified in this environment"
    )
