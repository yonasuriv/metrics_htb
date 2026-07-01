# Development

## Project layout

```
metrics-htb/
├── htb_machines.xlsx               # user spreadsheet (repo root, gitignored)
├── examples/sheets/
│   ├── htb_machines_template.xlsx  # headers-only template
│   └── htb_machines_example.xlsx   # sample data
└── src/htb_dashboard/
    ├── index.html                  # main page + styles + scripts
    ├── sheet.py                    # --new-sheet helper (used by htbm.py)
    └── assets/
        └── HackNerdFont-Regular.ttf
```

## Tech stack

| Layer | Technology |
|-------|------------|
| Layout | [Bootstrap 5](https://getbootstrap.com/) |
| Table | [DataTables](https://datatables.net/) |
| Excel parsing | [SheetJS / XLSX](https://sheetjs.com/) |
| Styling | Custom dark theme, matte badges, blur effects |
| Font | Hack Nerd Font (local TTF) |

## Data loading flow

1. `htbm.py dashboard --serve` serves `index.html` and `/htb_machines.xlsx` from the repo root
2. `index.html` fetches `htb_machines.xlsx` in the browser (or uses the offline file picker)
3. Each row becomes one completed machine record
4. `createTable()` converts parsed JSON to HTML with custom badges and styles
5. DataTables initializes search and pagination **without** re-sorting (preserves Excel order)
6. The manual upload card hides once a spreadsheet loads successfully

## Technique badges

`getTechBadge(tech)` generates a badge per technique:

- Matte colors per technique type
- `backdrop-filter: blur(8px)` for the frosted effect
- White text with shadow for contrast

## Credits

- Created and maintained by [yonasuriv](https://github.com/yonasuriv)
- Inspired by modern HTB dashboards and DataTables layouts

## License

Personal use — you may view, modify, and improve the dashboard for your own HTB tracking. Do not redistribute without the author's permission.

See [LICENSE](../../../LICENSE) for the repository license.
