from __future__ import annotations

import re
from pathlib import Path

USFM_SUFFIXES = {".usfm", ".sfm"}

CANONICAL_BOOK_IDS = {
    "gen",
    "exo",
    "lev",
    "num",
    "deu",
    "jos",
    "jdg",
    "rut",
    "1sa",
    "2sa",
    "1ki",
    "2ki",
    "1ch",
    "2ch",
    "ezr",
    "neh",
    "est",
    "job",
    "psa",
    "pro",
    "ecc",
    "sng",
    "isa",
    "jer",
    "lam",
    "ezk",
    "dan",
    "hos",
    "jol",
    "amo",
    "oba",
    "jon",
    "mic",
    "nam",
    "hab",
    "zep",
    "hag",
    "zec",
    "mal",
    "mat",
    "mrk",
    "luk",
    "jhn",
    "act",
    "rom",
    "1co",
    "2co",
    "gal",
    "eph",
    "php",
    "col",
    "1th",
    "2th",
    "1ti",
    "2ti",
    "tit",
    "phm",
    "heb",
    "jas",
    "1pe",
    "2pe",
    "1jn",
    "2jn",
    "3jn",
    "jud",
    "rev",
}


def discover_usfm_files(source_dir: Path) -> list[Path]:
    files = [
        path
        for path in sorted(source_dir.rglob("*"))
        if path.is_file() and path.suffix.lower() in USFM_SUFFIXES
    ]
    if not files:
        raise ValueError(f"No USFM files found in {source_dir}")
    return files


def normalize_book_id(raw: str) -> str | None:
    cleaned = re.sub(r"[^A-Za-z0-9]", "", raw or "").lower()
    if not cleaned:
        return None
    if cleaned in CANONICAL_BOOK_IDS:
        return cleaned
    if len(cleaned) >= 3 and cleaned[:3] in CANONICAL_BOOK_IDS:
        return cleaned[:3]
    order_prefixed = re.match(r"^\d{2}([a-z0-9]+)$", cleaned)
    if order_prefixed:
        without_order = order_prefixed.group(1)
        if without_order in CANONICAL_BOOK_IDS:
            return without_order
        if len(without_order) >= 3 and without_order[:3] in CANONICAL_BOOK_IDS:
            return without_order[:3]
        cleaned = without_order
    if len(cleaned) >= 3:
        candidate = cleaned[-3:]
        if candidate in CANONICAL_BOOK_IDS:
            return candidate
    return None


def infer_book_id(path: Path, usfm_text: str) -> str | None:
    from_name = normalize_book_id(path.stem)
    if from_name:
        return from_name
    match = re.search(r"(?m)^\s*\\id\s+([A-Za-z0-9]+)\b", usfm_text)
    if not match:
        return None
    return normalize_book_id(match.group(1))
