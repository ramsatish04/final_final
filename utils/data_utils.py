"""Utility helpers for data persistence and shared logic."""
import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def _file_path(filename: str) -> Path:
    """Return path to a data file inside DATA_DIR."""
    return DATA_DIR / filename

def ensure_data_file(filename: str, default: Any) -> None:
    """Create a data file with *default* content if it does not exist."""
    fp = _file_path(filename)
    if not fp.exists():
        save_data(default, filename)

def load_data(filename: str, default: Any):
    """Load JSON data; create with *default* if missing."""
    ensure_data_file(filename, default)
    with open(_file_path(filename), "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data: Any, filename: str) -> None:
    """Write JSON data atomically."""
    tmp = _file_path(filename).with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    tmp.replace(_file_path(filename))
