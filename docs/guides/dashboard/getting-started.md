# Getting started

Welcome to the **HTB Machines CheatSheet** — an interactive dashboard to visualize every Hack The Box machine you've pwned. Browse techniques used, difficulty, dates, and other details at a glance in your browser.

## What you get

- A searchable, paginated table of completed machines
- Color-coded difficulty and OS badges
- Technique tags with a matte blur effect
- Data loaded from a spreadsheet you control (`htb_machines_UPDATE.xlsx`)

## Quick start

From the **metrics-htb** repo:

```bash
git clone https://github.com/yonasuriv/metrics-htb.git
cd metrics-htb/src/htb_dashboard
```

Open `index.html` in a modern browser (local file or any static host).

Update `htb_machines_UPDATE.xlsx` as you complete new machines — reload the page to see changes.

> [!TIP]
> For a local dev server (avoids some browser file:// restrictions):

```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

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
