from __future__ import annotations

import argparse
from pathlib import Path

from .io_input import resolve_input_to_dir
from .util_paths import default_cache_dir


def build_command(args: argparse.Namespace) -> int:
    cache_dir = Path(args.cache_dir) if args.cache_dir else default_cache_dir()
    resolved_source_dir = resolve_input_to_dir(
        args.input, cache_dir=cache_dir, checksum_sha256=args.checksum_sha256
    )

    print(f"resolved_source_dir={resolved_source_dir}")
    print(f"translation={args.translation}")
    print(f"out={args.out}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="versecraft-build-db")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Resolve inputs and prepare build context")
    build_parser.add_argument("--translation", required=True, help="Translation key (e.g. bsb)")
    build_parser.add_argument("--input", required=True, help="Input directory, zip file, or zip URL")
    build_parser.add_argument("--out", required=True, help="Output SQLite path")
    build_parser.add_argument(
        "--cache-dir",
        default=None,
        help="Cache directory for downloads/extractions (default: tools/build_db/.cache)",
    )
    build_parser.add_argument(
        "--checksum-sha256",
        default=None,
        help="Optional SHA-256 checksum for zip input or download",
    )
    build_parser.add_argument(
        "--parser",
        choices=["auto", "grammar", "fallback"],
        default="auto",
        help="Parser selection (reserved for future use)",
    )
    build_parser.add_argument(
        "--no-sanity-check",
        action="store_true",
        help="Disable sanity check (reserved for future use)",
    )
    build_parser.add_argument("--sanity-book", default="jhn", help="Sanity check book ID")
    build_parser.add_argument("--sanity-chapter", type=int, default=3, help="Sanity check chapter")
    build_parser.add_argument(
        "--sanity-verses",
        default="16-18",
        help="Sanity check verses (e.g. 16-18)",
    )
    build_parser.set_defaults(func=build_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

