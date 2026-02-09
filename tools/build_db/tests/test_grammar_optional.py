from pathlib import Path

import pytest

from build_db.parse import parse_all


def test_grammar_parser_reads_fixture_when_installed() -> None:
    pytest.importorskip("usfm_grammar")
    fixture = Path(__file__).parent / "fixtures" / "jhn_min.usfm"
    records = parse_all([fixture], parser="grammar")
    assert any((record.book, record.chapter, record.verse) == ("jhn", 3, 16) for record in records)
