#!/usr/bin/env python3
import argparse
import json
import sqlite3
from pathlib import Path


META_FIELDS = [
    "translation_id",
    "name",
    "lang",
    "direction",
    "license",
    "source",
]


def _load_input(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS verses(
            book TEXT NOT NULL,
            chapter INTEGER NOT NULL,
            verse INTEGER NOT NULL,
            text TEXT NOT NULL,
            PRIMARY KEY(book, chapter, verse)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS meta(
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )


def _insert_meta(conn: sqlite3.Connection, payload: dict) -> None:
    meta_payload = payload.get("meta", {}) or {}
    translation_id = payload.get("translationId", "")
    values = {
        "translation_id": translation_id,
        "name": meta_payload.get("name", ""),
        "lang": meta_payload.get("lang", ""),
        "direction": meta_payload.get("direction", ""),
        "license": meta_payload.get("license", ""),
        "source": meta_payload.get("source", ""),
    }
    conn.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
        [(key, values.get(key, "")) for key in META_FIELDS],
    )


def _insert_verses(conn: sqlite3.Connection, payload: dict) -> None:
    verses = payload.get("verses", [])
    rows = [
        (v["book"], int(v["chapter"]), int(v["verse"]), v["text"])
        for v in verses
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO verses(book, chapter, verse, text) VALUES(?, ?, ?, ?)",
        rows,
    )


def build_db(input_path: Path, output_path: Path) -> None:
    payload = _load_input(input_path)
    _ensure_parent_dir(output_path)
    with sqlite3.connect(str(output_path)) as conn:
        _create_schema(conn)
        _insert_meta(conn, payload)
        _insert_verses(conn, payload)
        conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build VerseCraft SQLite DB.")
    parser.add_argument("--input", required=True, help="Path to input JSON file.")
    parser.add_argument("--output", required=True, help="Path to output SQLite DB.")
    args = parser.parse_args()

    build_db(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
