# Getting started

Welcome to the **HTB Machines CheatSheet** — an interactive dashboard to visualize every Hack The Box machine you've pwned. Browse techniques used, difficulty, dates, and other details at a glance in your browser.

## What you get

- A searchable, paginated table of completed machines
- Color-coded difficulty and OS badges
- Technique tags with a matte blur effect
- Data loaded from a spreadsheet you control (`htb_machines_UPDATE.xlsx`)

## Quick start

From the **metrics-htb** repo root:

```bash
python htbm.py dashboard --serve
# or offline mode (file picker for the spreadsheet):
python htbm.py dashboard
```

Update `src/htb_dashboard/htb_machines_UPDATE.xlsx` as you complete new machines — reload the page to see changes.

## Project layout

```
src/htb_dashboard/
├── index.html                  # Main page with interactive table
├── htb_machines_UPDATE.xlsx    # Machine data (your spreadsheet)
├── assets/
│   └── HackNerdFont-Regular.ttf
└── README.md                   # short overview → docs/guides/dashboard/
```

## Next steps

- [Features](features.md) — table columns, badges, DataTables, Excel loading
- [Customization](customization.md) — add techniques and tweak styles
- [Development](development.md) — tech stack and data flow
