# Development

## Project layout

```
metrics-htb/
└── src/htb_dashboard/
    ├── index.html                  # Main page + styles + scripts
    ├── htb_machines_UPDATE.xlsx      # Machine data spreadsheet
    ├── assets/
    │   └── HackNerdFont-Regular.ttf
    └── README.md                   # short overview → docs/guides/dashboard/
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

1. `index.html` fetches `htb_machines_UPDATE.xlsx` in the browser
2. Each row becomes one completed machine record
3. `createTable()` converts parsed JSON to HTML with custom badges and styles
4. DataTables initializes search and pagination **without** re-sorting (preserves Excel order)

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
