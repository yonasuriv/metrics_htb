# Development

## Project layout

```
metrics-htb/
├── htbm.py                  # unified entry point (metrics, cli, dashboard, setup)
├── generate.py              # backward-compatible alias → htbm metrics --generate
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
python htbm.py setup
source .venv/bin/activate
cp examples/config/.env.example .env   # optional, for local runs
```

## Run locally

```bash
python htbm.py metrics --pull -p YOUR_PROFILE_ID
python htbm.py metrics --generate -p YOUR_PROFILE_ID -t classic
python htbm.py metrics --generate --from-env
python htbm.py cli auth --token YOUR_TOKEN
python htbm.py dashboard --serve
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
| `test_examples.py` | Example templates, docs guides, htbm entry point |

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
