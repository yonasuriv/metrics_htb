from __future__ import annotations

import xml.sax.saxutils as xu
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

SHEET_HEADERS = (
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


def write_header_workbook(path: Path, headers: tuple[str, ...] = SHEET_HEADERS) -> None:
    """Write a header-only .xlsx workbook."""
    path.parent.mkdir(parents=True, exist_ok=True)

    sst_parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        (
            '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'count="{len(headers)}" uniqueCount="{len(headers)}">'
        ),
    ]
    for header in headers:
        sst_parts.append(f"<si><t>{xu.escape(header)}</t></si>")
    sst_parts.append("</sst>")

    cells = []
    for index in range(len(headers)):
        col = chr(ord("A") + index)
        cells.append(f'<c r="{col}1" t="s"><v>{index}</v></c>')
    sheet = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData><row r="1">{''.join(cells)}</row></sheetData>
</worksheet>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    wb_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>"""

    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets>
</workbook>"""

    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        archive.writestr("xl/worksheets/sheet1.xml", sheet)
        archive.writestr("xl/sharedStrings.xml", "".join(sst_parts))


def create_new_sheet(dest: Path | None = None, root: Path | None = None) -> Path:
    """Write a header-only htb_machines.xlsx at the repo root."""
    root = root or repo_root()
    dest = dest or default_sheet_path(root)
    if dest.exists():
        raise FileExistsError(f"Spreadsheet already exists: {dest}")
    write_header_workbook(dest)
    return dest
