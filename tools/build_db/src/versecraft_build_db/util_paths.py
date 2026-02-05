from __future__ import annotations

from pathlib import Path


def default_cache_dir() -> Path:
    tool_root = Path(__file__).resolve().parents[2]
    return tool_root / ".cache"
