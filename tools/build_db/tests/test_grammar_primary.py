from pathlib import Path

import pytest

from build_db.parse import parse_all


def test_grammar_parser_handles_complex_fixture_when_installed() -> None:
    pytest.importorskip("usfm_grammar")
    fixture = Path(__file__).parent / "fixtures" / "jhn_complex.usfm"
    records = parse_all([fixture], parser="grammar")
    by_ref = {(r.book, r.chapter, r.verse): r.text for r in records}

    assert ("jhn", 3, 16) in by_ref
    assert ("jhn", 3, 17) in by_ref
    assert "Footnote" not in by_ref[("jhn", 3, 16)]
    assert "Cross reference" not in by_ref[("jhn", 3, 17)]
    assert "one and only Son, that everyone who believes in him shall not perish." in by_ref[
        ("jhn", 3, 16)
    ]


def test_verify_parsers_passes_when_grammar_installed() -> None:
    pytest.importorskip("usfm_grammar")
    fixture = Path(__file__).parent / "fixtures" / "jhn_complex.usfm"
    records = parse_all([fixture], parser="grammar", verify_parsers=True)
    assert any((r.book, r.chapter, r.verse) == ("jhn", 3, 16) for r in records)
