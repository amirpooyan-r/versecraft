from pathlib import Path

from build_db.parse.fallback_parser import parse_file


def test_fallback_parser_reads_john_fixture() -> None:
    fixture = Path(__file__).parent / "fixtures" / "jhn_min.usfm"
    records = parse_file(fixture)
    lookup = {(r.book, r.chapter, r.verse): r.text for r in records}
    assert ("jhn", 3, 16) in lookup
    assert ("jhn", 3, 17) in lookup
    assert ("jhn", 3, 18) in lookup
    assert "Footnote" not in lookup[("jhn", 3, 16)]


def test_fallback_parser_handles_continuation_lines(tmp_path: Path) -> None:
    path = tmp_path / "44JHNTEST.SFM"
    path.write_text(
        "\\id JHN\n\\c 3\n\\v 16 First line.\nContinuation line.\n\\v 17 Next.\n",
        encoding="utf-8",
    )
    records = parse_file(path)
    verse_16 = next(record for record in records if record.verse == 16)
    assert verse_16.text == "First line. Continuation line."
