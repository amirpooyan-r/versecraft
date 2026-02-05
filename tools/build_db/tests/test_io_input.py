import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from versecraft_build_db.io_input import resolve_input_to_dir, safe_extract_zip


def test_safe_extract_zip_blocks_traversal(tmp_path: Path) -> None:
    zip_path = tmp_path / "evil.zip"
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("../evil.txt", "nope")

    dest_dir = tmp_path / "out"
    try:
        safe_extract_zip(zip_path, dest_dir)
        assert False, "Expected ValueError for unsafe zip entry"
    except ValueError as exc:
        assert "Unsafe zip entry" in str(exc) or "escapes destination" in str(exc)


def test_resolve_input_dir(tmp_path: Path) -> None:
    source_dir = tmp_path / "src"
    source_dir.mkdir()
    (source_dir / "44JHNTEST.SFM").write_text("\\id JHN\\n\\c 3\\n\\v 16 test\\n")

    resolved = resolve_input_to_dir(str(source_dir), cache_dir=tmp_path / "cache")
    assert resolved == source_dir


def test_resolve_input_zip(tmp_path: Path) -> None:
    fixture_zip = ROOT / "tests" / "fixtures" / "min_usfm.zip"
    resolved = resolve_input_to_dir(str(fixture_zip), cache_dir=tmp_path / "cache")

    assert resolved.exists()
    assert any(p.suffix.lower() in {".usfm", ".sfm"} for p in resolved.rglob("*"))
