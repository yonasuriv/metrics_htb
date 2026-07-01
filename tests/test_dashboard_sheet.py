from pathlib import Path

import pytest

from htb_dashboard.sheet import SHEET_HEADERS, create_new_sheet, template_path


def test_template_exists():
    assert template_path().is_file()


def test_create_new_sheet_writes_headers_only(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    template = root / "examples" / "sheets"
    template.mkdir(parents=True)
    source = template / "htb_machines_template.xlsx"
    source.write_bytes(template_path().read_bytes())

    dest = create_new_sheet(dest=root / "htb_machines.xlsx", root=root)
    assert dest.is_file()
    assert dest.stat().st_size > 0


def test_create_new_sheet_refuses_overwrite(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    template = root / "examples" / "sheets"
    template.mkdir(parents=True)
    source = template / "htb_machines_template.xlsx"
    source.write_bytes(template_path().read_bytes())
    dest = root / "htb_machines.xlsx"
    dest.write_text("existing")

    with pytest.raises(FileExistsError):
        create_new_sheet(dest=dest, root=root)


def test_sheet_headers_constant():
    assert "Nombre" in SHEET_HEADERS
    assert "URL" in SHEET_HEADERS
