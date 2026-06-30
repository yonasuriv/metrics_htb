# Examples

Sample outputs and copy-paste templates for HTB Metrics. Nothing in this directory runs automatically from the repository.

## Layout

```
examples/
├── badges/                   # preview only — do NOT copy to your repo
│   └── htb-metrics.*.png     # sample rendered badges per template
├── config/                   # copy these to your project root
│   ├── .env.example          → .env
│   └── htb-metrics.yml.example → htb-metrics.yml
└── workflows/                # copy one to .github/workflows/
    ├── htb-metrics-consumer.yml
    ├── htb-metrics-fork.yml
    └── README.md
```

## Badge previews (`badges/`)

PNG/SVG files under `examples/badges/` are **reference renders only** — for README previews and template comparison. They are **not** templates and should **not** be copied into your profile repo.

Your own badges are generated into `output/` when you run the generator locally or via GitHub Actions.

## Config examples (`config/`)

Copy to the **repository root** (not into `examples/`):

```bash
cp examples/config/.env.example .env
cp examples/config/htb-metrics.yml.example htb-metrics.yml
```

Edit at least `HTB_PROFILE_ID`. See [Configuration](../docs/guides/configuration.md).

## Workflow templates (`workflows/`)

Copy **one** file to `.github/workflows/htb-metrics.yml` in your profile repo.

See [GitHub Actions](../docs/guides/github-actions.md) or [workflows/README.md](workflows/README.md).

## Raw URLs (GitHub)

Replace `main` with a tag or SHA to pin a version.

| File | URL |
|------|-----|
| Consumer workflow | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/examples/workflows/htb-metrics-consumer.yml` |
| Fork workflow | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/examples/workflows/htb-metrics-fork.yml` |
| `.env` example | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/examples/config/.env.example` |
| YAML example | `https://raw.githubusercontent.com/yonasuriv/metrics-htb/main/examples/config/htb-metrics.yml.example` |

Badge previews are not published as raw URLs — browse [`examples/badges/`](badges/) in the repo.
