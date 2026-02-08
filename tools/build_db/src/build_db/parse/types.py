from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VerseRecord:
    book: str
    chapter: int
    verse: int
    text: str


class ParseError(Exception):
    """Raised when USFM parsing fails."""
