# Development

## Project layout

```
htb-ctrl/
├── htbctrl.py                  # unified entry point (auto-bootstrap)
├── pyproject.toml              # package + pytest config
├── requirements.txt            # -e . + dev deps
├── src/
│   ├── ctrl_metrics/           # badge generator + metrics pull
│   ├── ctrl_cli/               # Typer CLI (terminal, metrics, badges, dashboard)
│   ├── ctrl_dashboard/         # browser cheat sheet
│   └── ctrl_config/            # SSOT config + auth resolution
├── user/                       # per-profile data + badges (gitignored)
│   └── <profile_id>/
│       ├── data/               # cached HTB API JSON
│       └── badges/             # generated PNG/SVG
├── assets/templates/           # HTML + SVG badge templates
├── examples/                   # config + workflow templates; badge previews
├── docs/                       # user documentation
└── tests/
```

## Setup

```bash
htbctrl --help
source .venv/bin/activate
```

## Run locally

```bash
htbctrl metrics pull -p YOUR_PROFILE_ID
htbctrl badges generate -p YOUR_PROFILE_ID -t classic
htbctrl badges generate --from-env
htbctrl auth --token YOUR_TOKEN
htbctrl dashboard --serve
htb-ctrl --help                  # after pip install -e .
```

## Tests

```bash
python -m pytest tests/ --ignore=tests/test_e2e.py
```

| Test file | Covers |
|-----------|--------|
| `test_config.py` | Config loading, auth token resolution, `--from-env`, user paths |
| `test_fetch.py` | API fetch (mocked with `responses`) |
| `test_dataset.py` | Dataset normalization |
| `test_render.py` | Template `$placeholder$` injection |
| `test_paths.py` | User dir layout, asset paths |
| `test_examples.py` | Example templates, docs guides, htbctrl entry point |

Live API e2e (optional):

```bash
HTB_E2E=1 python -m pytest tests/test_e2e.py
```

## Adding a template

1. Add `assets/templates/html/your-template.html` or `assets/templates/svg/your-template.svg`
2. Use `$field$` placeholders — see [Templates](badge-templates.md)
3. HTML templates need a `.badge` root element for Playwright screenshot
4. Template name is the filename stem; discovered automatically by `config.py`

## Icons

Vendor icons live under `assets/vendor/icons/`. Refresh from HTB CDN when adding new template fields that reference icons.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md).
