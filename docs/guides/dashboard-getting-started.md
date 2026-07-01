# Getting started

Welcome to the **HTB Machines CheatSheet** — an interactive dashboard to visualize every Hack The Box machine you've pwned. Browse techniques used, difficulty, dates, and other details at a glance in your browser.

## What you get

- A searchable, paginated table of completed machines
- Color-coded difficulty and OS badges
- Technique tags with a matte blur effect
- Data loaded from a spreadsheet you control (`htb_machines.xlsx` at the repo root)

## Quick start

From the **htb-ctrl** repo root:

```bash
htbctrl dashboard --new-sheet    # create header-only htb_machines.xlsx
htbctrl dashboard --serve        # local server + auto-load spreadsheet
# or offline mode (file picker for the spreadsheet):
htbctrl dashboard
```

Update `htb_machines.xlsx` as you complete new machines — reload the page to see changes.

Sample data format: [`examples/sheets/htb_machines_example.xlsx`](../../examples/sheets/htb_machines_example.xlsx)

## Project layout

```
htb_machines.xlsx               # your machine log (repo root, gitignored)
examples/sheets/
├── htb_machines_template.xlsx  # headers-only template (--new-sheet source)
└── htb_machines_example.xlsx   # sample rows for reference
src/ctrl_dashboard/
├── index.html                  # main page with interactive table
└── assets/
    └── HackNerdFont-Regular.ttf
```

## Next steps

- [Features](dashboard-features.md) — table columns, badges, DataTables, Excel loading
- [Customization](dashboard-customization.md) — add techniques and tweak styles
- [Development](dashboard-development.md) — tech stack and data flow
