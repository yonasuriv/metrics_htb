# Development

## Project layout

```
htb-ctrl/
├── htbctrl.py                  # unified entry point (metrics, cli, dashboard, setup)
├── generate.py              # backward-compatible alias → htbctrl metrics --generate
├── pyproject.toml           # package + pytest config
├── requirements.txt         # -e . + dev deps
├── src/
│   ├── htb_metrics/         # badge generator
│   ├── htb_cli/             # terminal CLI
│   └── htb_dashboard/       # browser cheat sheet
├── user/                    # per-profile data + badges (gitignored)
│   └── <profile_id>/
│       ├── data/            # cached HTB API JSON
│       └── badges/          # generated PNG/SVG
├── assets/templates/        # HTML + SVG badge templates
├── examples/                # config + workflow templates; badge previews
├── docs/                    # user documentation
└── tests/
```

## Setup

```bash
python htbctrl.py setup --init
source .venv/bin/activate
```

## Run locally

```bash
python htbctrl.py metrics --pull -p YOUR_PROFILE_ID
python htbctrl.py metrics --generate -p YOUR_PROFILE_ID -t classic
python htbctrl.py metrics --generate --from-env
python htbctrl.py cli auth --token YOUR_TOKEN
python htbctrl.py dashboard --serve
htb-metrics --help                  # after pip install -e .
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
2. Use `$field$` placeholders — see [Templates](templates.md)
3. HTML templates need a `.badge` root element for Playwright screenshot
4. Template name is the filename stem; discovered automatically by `config.py`

## Icons

Vendor icons live under `assets/vendor/icons/`. Refresh from HTB CDN:

```bash
python scripts/download_icons.py
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).
