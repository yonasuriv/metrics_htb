# Features

## Machine listing

The table shows every machine you've completed on HTB, including:

- **Machine name** (bold)
- **Difficulty** — Easy, Intermediate, Hard, Insane with color badges
- **Status** — Active / Inactive
- **Done** — Completed or not
- **OS** — Windows or Linux badges
- **URL** — Machine page or writeup link
- **Techniques** — Visual badges (`sqli`, `xss`, `proxy`, `subdomains`, `python3`, etc.)
- **Completion date**

## Visual badges

### Techniques

Techniques render as matte-colored badges with a **blur effect** (`backdrop-filter`) for readability on the dark theme.

### Difficulty colors

| Difficulty | Color |
|------------|-------|
| Easy | Green |
| Intermediate | Yellow |
| Hard | Red |
| Insane | Purple |

### OS colors

| OS | Color |
|----|-------|
| Windows | Blue |
| Orange | Linux |

## Interactive table (DataTables)

- **Quick search** across all columns
- **Pagination** for large lists
- Dark modern styling
- **No automatic sort** — the table preserves Excel row order (`htb_machines_UPDATE.xlsx`), so machines appear in the same sequence you recorded them

## Excel data source

The page loads data from `htb_machines_UPDATE.xlsx` via [SheetJS / XLSX](https://sheetjs.com/) in the browser. Edit the spreadsheet, save, and reload — no rebuild required.

## See also

- [Customization](customization.md) — add new technique badges
- [Development](development.md) — `createTable()` and data pipeline
