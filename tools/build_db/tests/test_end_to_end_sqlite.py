from __future__ import annotations

import sqlite3
from pathlib import Path
from zipfile import ZipFile

from build_db.cli import main
from build_db.io import safe_extract_zip


def _fixture_dir(tmp_path: Path) -> Path:
    source_dir = tmp_path / "input"
    source_dir.mkdir()
    fixture = Path(__file__).parent / "fixtures" / "jhn_min.usfm"
    (source_dir / "44JHNTEST.SFM").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    return source_dir


def test_build_pipeline_dir_input(tmp_path: Path) -> None:
    source_dir = _fixture_dir(tmp_path)
    out_path = tmp_path / "out" / "jhn.sqlite"
    exit_code = main(
        [
            "--input",
            str(source_dir),
            "--out",
            str(out_path),
            "--translation-id",
            "KJV",
            "--translation-name",
            "King James Version",
            "--parser",
            "fallback",
        ]
    )
    assert exit_code == 0
    with sqlite3.connect(out_path) as conn:
        rows = conn.execute(
            "SELECT verse, text FROM verses WHERE book=? AND chapter=? ORDER BY verse",
            ("jhn", 3),
        ).fetchall()
        meta_lang = conn.execute("SELECT value FROM meta WHERE key='lang'").fetchone()
    assert [row[0] for row in rows] == [16, 17, 18]
    assert all(str(row[1]).strip() for row in rows)
    assert meta_lang == ("en",)


def test_build_pipeline_zip_input(tmp_path: Path) -> None:
    source_dir = _fixture_dir(tmp_path)
    zip_path = tmp_path / "jhn.zip"
    with ZipFile(zip_path, "w") as archive:
        archive.write(source_dir / "44JHNTEST.SFM", arcname="44JHNTEST.SFM")
    out_path = tmp_path / "out" / "from_zip.sqlite"
    exit_code = main(
        [
            "--input",
            str(zip_path),
            "--out",
            str(out_path),
            "--translation-id",
            "BSB",
            "--translation-name",
            "Berean Standard Bible",
            "--parser",
            "fallback",
            "--sanity",
            "jhn 3:16-18",
        ]
    )
    assert exit_code == 0
    assert out_path.exists()


def test_safe_extract_blocks_zip_slip(tmp_path: Path) -> None:
    archive_path = tmp_path / "evil.zip"
    with ZipFile(archive_path, "w") as archive:
        archive.writestr("../escape.txt", "blocked")
    target_dir = tmp_path / "out"
    try:
        safe_extract_zip(archive_path, target_dir)
        assert False, "expected zip-slip protection failure"
    except ValueError as exc:
        assert "Unsafe zip entry" in str(exc)
