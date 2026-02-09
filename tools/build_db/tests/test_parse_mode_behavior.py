from pathlib import Path

import pytest

from build_db.parse import parse_all
from build_db.parse.types import ParseError, VerseRecord


def test_auto_mode_uses_fallback_without_grammar_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = [VerseRecord(book="jhn", chapter=3, verse=16, text="fallback")]

    def _raise_if_called(_path: Path) -> list[VerseRecord]:
        raise AssertionError("grammar should not run in auto mode unless verify_parsers is enabled")

    def _fallback(_path: Path) -> list[VerseRecord]:
        return expected

    monkeypatch.setattr("build_db.parse.parse_file_grammar", _raise_if_called)
    monkeypatch.setattr("build_db.parse.parse_file_fallback", _fallback)

    records = parse_all([Path("dummy.usfm")], parser="auto")

    assert records == expected


def test_grammar_mode_propagates_parseerror_without_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    message = "usfm-grammar integration not implemented yet; use --parser fallback"

    def _raise_parse_error(_path: Path) -> list[VerseRecord]:
        raise ParseError(message)

    def _fallback(_path: Path) -> list[VerseRecord]:
        raise AssertionError("fallback must not run in grammar mode")

    monkeypatch.setattr("build_db.parse.parse_file_grammar", _raise_parse_error)
    monkeypatch.setattr("build_db.parse.parse_file_fallback", _fallback)

    with pytest.raises(ParseError, match="not implemented yet"):
        parse_all([Path("dummy.usfm")], parser="grammar")


def test_auto_verify_skips_grammar_when_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = [VerseRecord(book="jhn", chapter=3, verse=16, text="fallback")]

    def _raise_if_called(_path: Path) -> list[VerseRecord]:
        raise AssertionError("grammar should be skipped when unavailable")

    def _fallback(_path: Path) -> list[VerseRecord]:
        return expected

    monkeypatch.setattr("build_db.parse._has_usfm_grammar", lambda: False)
    monkeypatch.setattr("build_db.parse.parse_file_grammar", _raise_if_called)
    monkeypatch.setattr("build_db.parse.parse_file_fallback", _fallback)

    records = parse_all([Path("dummy.usfm")], parser="auto", verify_parsers=True)

    assert records == expected
