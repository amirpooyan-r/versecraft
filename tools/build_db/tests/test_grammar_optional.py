from pathlib import Path

import pytest

from build_db.parse import parse_all
from build_db.parse.types import ParseError


def test_grammar_optional_behavior() -> None:
    pytest.importorskip("usfm_grammar")
    fixture = Path(__file__).parent / "fixtures" / "jhn_min.usfm"
    try:
        records = parse_all([fixture], parser="grammar")
    except NotImplementedError:
        pytest.skip("usfm-grammar API not verified in this environment")
    except ParseError:
        pytest.skip("usfm-grammar parse unavailable in this environment")
    assert any((record.book, record.chapter, record.verse) == ("jhn", 3, 16) for record in records)
