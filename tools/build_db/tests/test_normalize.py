from build_db.parse.normalize import normalize_verse_text


def test_normalize_removes_footnotes_and_xrefs() -> None:
    text = (
        r"For God so loved the world \f + \ft Footnote \f* and"
        r" sent his Son \x + \xo 3:16 \xt ref \x*."
    )
    result = normalize_verse_text(text)
    assert "Footnote" not in result
    assert "xo" not in result
    assert result == "For God so loved the world and sent his Son ."


def test_normalize_collapses_whitespace() -> None:
    result = normalize_verse_text(" A   verse\twith\nmany  spaces ")
    assert result == "A verse with many spaces"
