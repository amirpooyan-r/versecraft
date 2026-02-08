import pytest

from build_db.parse.types import VerseRecord
from build_db.validate import validate_records


def test_validate_rejects_empty() -> None:
    with pytest.raises(ValueError, match="No verses extracted"):
        validate_records([])


def test_validate_rejects_duplicates() -> None:
    records = [
        VerseRecord(book="jhn", chapter=3, verse=16, text="a"),
        VerseRecord(book="jhn", chapter=3, verse=16, text="b"),
    ]
    with pytest.raises(ValueError, match="Duplicate verse reference"):
        validate_records(records)
