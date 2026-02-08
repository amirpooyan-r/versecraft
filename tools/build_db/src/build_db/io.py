from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from tempfile import mkdtemp
from urllib.parse import urlparse
from urllib.request import urlopen
from zipfile import ZipFile


@dataclass
class InputSource:
    source_dir: Path
    temp_dir: Path | None = None

    def cleanup(self) -> None:
        if self.temp_dir is None:
            return
        for path in sorted(self.temp_dir.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        self.temp_dir.rmdir()


def _is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def safe_extract_zip(zip_path: Path, dest_dir: Path) -> None:
    destination = dest_dir.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = PurePosixPath(member.filename)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"Unsafe zip entry: {member.filename}")
            target = (destination / member_path).resolve()
            if not target.is_relative_to(destination):
                raise ValueError(f"Zip entry escapes destination: {member.filename}")
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target.open("wb") as out:
                out.write(source.read())


def _download_zip(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url, timeout=60) as response, target.open("wb") as out:
        out.write(response.read())


def open_input_source(input_value: str) -> InputSource:
    input_path = Path(input_value)
    if input_path.is_dir():
        return InputSource(source_dir=input_path)
    if input_path.is_file() and input_path.suffix.lower() == ".zip":
        temp_dir = Path(mkdtemp(prefix="build_db_"))
        source_dir = temp_dir / "input"
        safe_extract_zip(input_path, source_dir)
        return InputSource(source_dir=source_dir, temp_dir=temp_dir)
    if _is_url(input_value):
        parsed = urlparse(input_value)
        if not parsed.path.lower().endswith(".zip"):
            raise ValueError("URL input must point to a .zip file")
        temp_dir = Path(mkdtemp(prefix="build_db_"))
        zip_path = temp_dir / "download.zip"
        source_dir = temp_dir / "input"
        _download_zip(input_value, zip_path)
        safe_extract_zip(zip_path, source_dir)
        return InputSource(source_dir=source_dir, temp_dir=temp_dir)
    raise ValueError(f"Unsupported input: {input_value}")
