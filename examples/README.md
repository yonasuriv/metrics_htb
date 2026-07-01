# Examples

Sample outputs and copy-paste templates for HTB Metrics. Nothing in this directory runs automatically from the repository.

## Layout

```
examples/
├── badges/                   # preview only — do NOT copy to your repo
│   └── htb-metrics.*.png     # sample rendered badges per template
├── config/                   # copy these to your project root
│   ├── .env.example          → .env
│   ├── htb-metrics.yml.example → htb-metrics.yml
│   └── htb-cli.yml.example   → htb-cli.yml
├── sheets/                   # dashboard spreadsheet templates
│   ├── htb_machines_template.xlsx  # headers only (--new-sheet source)
│   └── htb_machines_example.xlsx   # sample rows (reference only)
└── workflows/                # copy one to .github/workflows/
    ├── htb-metrics-consumer.yml
    ├── htb-metrics-fork.yml
    └── README.md
```

## Badge previews (`badges/`)

PNG/SVG files under `examples/badges/` are **reference renders only** — for README previews and template comparison. They are **not** templates and should **not** be copied into your profile repo.

Your own badges are generated into `user/<profile_id>/badges/` when you run the generator locally or via GitHub Actions.

## Config examples (`config/`)

Copy to the **repository root** (not into `examples/`):

```bash
cp examples/config/.env.example .env
cp examples/config/htb-metrics.yml.example htb-metrics.yml
cp examples/config/htb-cli.yml.example htb-cli.yml   # optional CLI token YAML
```

Edit at least `HTB_PROFILE_ID` for metrics. Token env vars (`HTB_API_TOKEN`, etc.) are shared by metrics and CLI. See [Configuration](../docs/guides/badge/configuration.md) and [CLI configuration](../docs/guides/cli/configuration.md).

## Dashboard sheets (`sheets/`)

Create your own log at the repo root:

```bash
python htbctrl.py dashboard --new-sheet   # writes htb_machines.xlsx (headers only)
```

Use `htb_machines_example.xlsx` as a format reference — do not copy it to the repo root unless you want sample data.

## Workflow templates (`workflows/`)

Copy **one** file to `.github/workflows/htb-metrics.yml` in your profile repo.

See [GitHub Actions](../docs/guides/badge/github-actions.md) or [workflows/README.md](workflows/README.md).

## Raw URLs (GitHub)

Replace `main` with a tag or SHA to pin a version.

| File | URL |
|------|-----|
| Consumer workflow | `https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/workflows/htb-metrics-consumer.yml` |
| Fork workflow | `https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/workflows/htb-metrics-fork.yml` |
| `.env` example | `https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/config/.env.example` |
| YAML example | `https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/config/htb-metrics.yml.example` |
| CLI YAML example | `https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/examples/config/htb-cli.yml.example` |

Badge previews are not published as raw URLs — browse [`examples/badges/`](badges/) in the repo.
