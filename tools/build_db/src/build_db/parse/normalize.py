from __future__ import annotations

import re

_FOOTNOTE_RE = re.compile(r"\\f\b.*?\\f\*", re.DOTALL)
_XREF_RE = re.compile(r"\\x\b.*?\\x\*", re.DOTALL)
_INLINE_MARKER_RE = re.compile(r"\\[A-Za-z0-9][A-Za-z0-9-]*\*?")
_WS_RE = re.compile(r"\s+")


def normalize_verse_text(text: str) -> str:
    if not text:
        return ""
    value = _FOOTNOTE_RE.sub(" ", text)
    value = _XREF_RE.sub(" ", value)
    # Keep payload text but remove marker tokens.
    value = _INLINE_MARKER_RE.sub(" ", value)
    return _WS_RE.sub(" ", value).strip()
