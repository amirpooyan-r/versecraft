from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .discover import discover_usfm_files
from .io import open_input_source
from .parse import parse_all
from .sanity import run_sanity_check
from .sqlite_writer import write_sqlite
from .validate import validate_records


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="build-db")
    parser.add_argument("--input", required=True, help="Input directory, zip path, or zip URL")
    parser.add_argument("--out", required=True, help="Output sqlite path")
    parser.add_argument("--translation-id", required=True, help="Translation id (for meta table)")
    parser.add_argument("--translation-name", required=True, help="Translation name")
    parser.add_argument("--lang", default="en", help="Language code (default: en)")
    parser.add_argument(
        "--parser",
        default="auto",
        choices=["auto", "grammar", "fallback"],
        help="Parser mode (default: auto)",
    )
    parser.add_argument(
        "--sanity",
        default="jhn 3:16-18",
        help='Sanity check reference, e.g. "jhn 3:16-18"',
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    source = open_input_source(args.input)
    try:
        usfm_files = discover_usfm_files(source.source_dir)
        records = parse_all(usfm_files, parser=args.parser)
        validate_records(records)
        records = sorted(records, key=lambda r: (r.book, r.chapter, r.verse))
        meta = {
            "translation_id": args.translation_id,
            "translation_name": args.translation_name,
            "lang": args.lang,
            "schema_version": "1",
            "tool": "build_db",
            "tool_version": __version__,
            "created_utc": datetime.now(timezone.utc).isoformat(),
        }
        out_path = Path(args.out)
        write_sqlite(out_path, records, meta)
        run_sanity_check(out_path, args.sanity)
    except Exception as exc:
        print(f"error: {exc}")
        return 1
    finally:
        source.cleanup()

    print(
        f"built {len(records)} verses "
        f"for {args.translation_id} with parser={args.parser} at {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
