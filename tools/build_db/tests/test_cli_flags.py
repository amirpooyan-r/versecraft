from __future__ import annotations

from pathlib import Path

import pytest

from build_db.cli import main


def _fixture_dir(tmp_path: Path, fixture_name: str = "jhn_min.usfm") -> Path:
    source_dir = tmp_path / "input"
    source_dir.mkdir()
    fixture = Path(__file__).parent / "fixtures" / fixture_name
    (source_dir / "44JHNTEST.SFM").write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    return source_dir


def test_auto_mode_defaults_to_fallback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_dir = _fixture_dir(tmp_path)

    def _raise_if_called(_path: Path) -> list[object]:
        raise AssertionError("grammar parser should not run in default auto mode")

    monkeypatch.setattr("build_db.parse.parse_file_grammar", _raise_if_called)

    out_ok = tmp_path / "out" / "auto_default.sqlite"
    exit_ok = main(
        [
            "--input",
            str(source_dir),
            "--out",
            str(out_ok),
            "--translation-id",
            "KJV",
            "--translation-name",
            "King James Version",
            "--parser",
            "auto",
        ]
    )
    assert exit_ok == 0
    assert out_ok.exists()


def test_verify_parsers_flag_passes_when_grammar_installed(tmp_path: Path) -> None:
    pytest.importorskip("usfm_grammar")
    source_dir = _fixture_dir(tmp_path, fixture_name="jhn_complex.usfm")
    out_path = tmp_path / "out" / "verify.sqlite"
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
            "grammar",
            "--verify-parsers",
            "--sanity",
            "jhn 3:16-17",
        ]
    )
    assert exit_code == 0


def test_auto_verify_skips_grammar_when_unavailable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_dir = _fixture_dir(tmp_path, fixture_name="jhn_complex.usfm")
    monkeypatch.setattr("build_db.parse._has_usfm_grammar", lambda: False)

    def _raise_if_called(_path: Path) -> list[object]:
        raise AssertionError("grammar parser should not run when module is unavailable")

    monkeypatch.setattr("build_db.parse.parse_file_grammar", _raise_if_called)

    out_path = tmp_path / "out" / "verify_auto.sqlite"
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
            "auto",
            "--verify-parsers",
            "--sanity",
            "jhn 3:16-17",
        ]
    )
    assert exit_code == 0
