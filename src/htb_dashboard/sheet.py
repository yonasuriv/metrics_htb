from __future__ import annotations

import shutil
from pathlib import Path

SHEET_HEADERS = (
    "Nombre",
    "Titulo",
    "OS",
    "Dificultad",
    "Tecnicas",
    "Fecha",
    "Activa",
    "URL",
    "Hecha",
)
DEFAULT_SHEET_NAME = "htb_machines.xlsx"
TEMPLATE_NAME = "htb_machines_template.xlsx"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def template_path(root: Path | None = None) -> Path:
    root = root or repo_root()
    return root / "examples" / "sheets" / TEMPLATE_NAME


def default_sheet_path(root: Path | None = None) -> Path:
    root = root or repo_root()
    return root / DEFAULT_SHEET_NAME


def create_new_sheet(dest: Path | None = None, root: Path | None = None) -> Path:
    """Write a header-only htb_machines.xlsx at the repo root."""
    root = root or repo_root()
    dest = dest or default_sheet_path(root)
    source = template_path(root)
    if not source.is_file():
        raise FileNotFoundError(f"Sheet template not found: {source}")
    if dest.exists():
        raise FileExistsError(f"Spreadsheet already exists: {dest}")
    shutil.copy2(source, dest)
    return dest
