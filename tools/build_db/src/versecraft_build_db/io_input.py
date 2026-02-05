from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse
from zipfile import ZipFile

import requests

USFM_EXTS = {".usfm", ".sfm"}


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def download_url_to_file(url: str, dest_path: Path) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with dest_path.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path: Path, expected_hex: str) -> None:
    actual = sha256_file(path)
    if actual.lower() != expected_hex.lower():
        raise ValueError(f"SHA-256 mismatch for {path}: expected {expected_hex}, got {actual}")


def safe_extract_zip(zip_path: Path, dest_dir: Path) -> None:
    dest_dir = dest_dir.resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path) as zf:
        for member in zf.infolist():
            name = member.filename
            posix_path = PurePosixPath(name)
            if posix_path.is_absolute() or ".." in posix_path.parts:
                raise ValueError(f"Unsafe zip entry: {name}")

            target_path = (dest_dir / posix_path).resolve()
            if not target_path.is_relative_to(dest_dir):
                raise ValueError(f"Zip entry escapes destination: {name}")

            if member.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member, "r") as source, target_path.open("wb") as dest:
                for chunk in iter(lambda: source.read(1024 * 1024), b""):
                    dest.write(chunk)


def _contains_usfm_files(path: Path) -> bool:
    for file_path in path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in USFM_EXTS:
            return True
    return False


def _extract_zip_to_cache(zip_path: Path, cache_dir: Path) -> Path:
    extracted_root = cache_dir / "extracted"
    zip_hash = sha256_file(zip_path)[:16]
    dest_dir = extracted_root / zip_hash

    if dest_dir.exists() and _contains_usfm_files(dest_dir):
        return dest_dir

    if dest_dir.exists():
        for item in dest_dir.rglob("*"):
            if item.is_file():
                item.unlink()
        for item in sorted(dest_dir.rglob("*"), reverse=True):
            if item.is_dir():
                item.rmdir()

    safe_extract_zip(zip_path, dest_dir)
    return dest_dir


def resolve_input_to_dir(
    input_value: str, cache_dir: Path, checksum_sha256: str | None = None
) -> Path:
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    if is_url(input_value):
        parsed = urlparse(input_value)
        name = Path(parsed.path).name or "download"
        if not name.lower().endswith(".zip"):
            name = f"{name}.zip"
        url_id = hashlib.sha256(input_value.encode("utf-8")).hexdigest()[:12]
        download_path = cache_dir / "downloads" / f"{Path(name).stem}_{url_id}.zip"
        download_url_to_file(input_value, download_path)
        if checksum_sha256:
            verify_sha256(download_path, checksum_sha256)
        extracted_dir = _extract_zip_to_cache(download_path, cache_dir)
        if not _contains_usfm_files(extracted_dir):
            raise ValueError(f"No USFM/SFM files found in extracted directory: {extracted_dir}")
        return extracted_dir

    input_path = Path(input_value)
    if input_path.is_dir():
        if not _contains_usfm_files(input_path):
            raise ValueError(f"No USFM/SFM files found in directory: {input_path}")
        return input_path

    if input_path.is_file() and input_path.suffix.lower() == ".zip":
        if checksum_sha256:
            verify_sha256(input_path, checksum_sha256)
        extracted_dir = _extract_zip_to_cache(input_path, cache_dir)
        if not _contains_usfm_files(extracted_dir):
            raise ValueError(f"No USFM/SFM files found in extracted directory: {extracted_dir}")
        return extracted_dir

    raise ValueError(f"Unsupported input path: {input_value}")
