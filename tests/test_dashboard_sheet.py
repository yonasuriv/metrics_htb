from pathlib import Path

import pytest

from ctrl_dashboard.sheet import SHEET_HEADERS, create_new_sheet, write_header_workbook


def test_create_new_sheet_writes_headers_only(tmp_path):
    dest = tmp_path / "htb_machines.xlsx"
    created = create_new_sheet(dest=dest, root=tmp_path)
    assert created.is_file()
    assert created.stat().st_size > 0


def test_create_new_sheet_refuses_overwrite(tmp_path):
    dest = tmp_path / "htb_machines.xlsx"
    dest.write_text("existing")

    with pytest.raises(FileExistsError):
        create_new_sheet(dest=dest, root=tmp_path)


def test_sheet_headers_are_english():
    assert SHEET_HEADERS == (
        "Name",
        "Title",
        "OS",
        "Difficulty",
        "Techniques",
        "Date",
        "Active",
        "URL",
        "Done",
    )


def test_write_header_workbook(tmp_path):
    path = tmp_path / "test.xlsx"
    write_header_workbook(path)
    assert path.is_file()
