# Development

## Project layout

```
metrics-htb/
├── generate.py              # CLI entry (adds src/ to sys.path)
├── pyproject.toml           # package + pytest config
├── requirements.txt         # -e . + dev deps
├── src/htb_metrics/
│   ├── cli.py               # main entry
│   ├── config.py            # CLI / env / YAML loading
│   ├── fetch.py             # HTB API client
│   ├── dataset.py           # raw → template dict
│   ├── render.py            # HTML/SVG → PNG (Playwright)
│   └── paths.py             # repo-root asset paths
├── assets/templates/        # HTML + SVG badge templates
├── refs/                    # copy-paste templates (workflows, config)
├── docs/                    # user documentation
├── tests/
└── output/                  # generated badges (local)
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp refs/config/.env.example .env   # optional, for local runs
```

## Run locally

```bash
python generate.py -p YOUR_PROFILE_ID -t classic
python generate.py --from-env
htb-metrics --help                  # after pip install -e .
```

## Tests

```bash
python -m pytest tests/ --ignore=tests/test_e2e.py
```

| Test file | Covers |
|-----------|--------|
| `test_config.py` | Config loading, auth token resolution, `--from-env` |
| `test_fetch.py` | API fetch (mocked with `responses`) |
| `test_dataset.py` | Dataset normalization |
| `test_render.py` | Template `$placeholder$` injection |
| `test_paths.py` | Src layout asset paths |
| `test_refs.py` | Reference templates exist |

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

See [CONTRIBUTING.md](../CONTRIBUTING.md).
