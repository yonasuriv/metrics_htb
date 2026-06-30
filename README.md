<div align="center" id="madewithlua">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset=".github/assets/metrics-light.png">
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/metrics-dark.png">
    <img src=".github/assets/metrics-dark.png" alt="HTB Metrics">
  </picture>
  <picture>
    <img src=".github/assets/htb.png" alt="Hack The Box">
  </picture>
  <h2>Metrics HTB</h2>
</div>

Auto-generated **Hack The Box profile badges** for your GitHub README — legacy rank, experience level, season league, flags, and more. Updated daily via GitHub Actions.

![HTB Metrics classic badge](examples/badges/htb-metrics.classic.png)

## Features

- **12 templates** — classic, terminal, GitHub-style cards, minimal badge, and more
- **Public + optional auth** — works with a public profile; app token unlocks extra API data
- **No fork required** — copy a workflow template into your profile repo
- **Local dev** — `.env`, YAML, or CLI flags

## Templates

| Name | Style |
|------|--------|
| `classic` | HTB dark — avatar, stats, ranking |
| `compact` | Single-row card |
| `profile-card` | Full stats grid + rank tiers |
| `rank-card` | Legacy / level / season focus |
| `season-card` | Current season highlight |
| `terminal` | Kali terminal aesthetic |
| `hacker-red` / `hacker-yellow` | Accent themes |
| `light` / `minimal` | Light / inline badge |
| `github-classic` / `github-plugin` | GitHub-style cards |

See [Template placeholders](docs/guides/templates.md) for all `$fields$`. Preview renders live in [`examples/badges/`](examples/badges/) (reference only — do not copy).

## Quick start

```bash
git clone https://github.com/yonasuriv/metrics-htb.git && cd metrics-htb
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && playwright install chromium
cp examples/config/.env.example .env   # set HTB_PROFILE_ID
python generate.py --from-env
```

For GitHub Actions (no fork): [Getting started → GitHub Actions](docs/guides/getting-started.md#github-actions-no-fork).

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting started](docs/guides/getting-started.md) | Install, first badge, GitHub Actions |
| [Configuration](docs/guides/configuration.md) | CLI, env, YAML, secrets, cache |
| [GitHub Actions](docs/guides/github-actions.md) | Workflow templates in `examples/workflows/` |
| [Templates](docs/guides/templates.md) | Placeholders and template list |
| [Data sources](docs/guides/data-sources.md) | HTB API endpoints |
| [Development](docs/guides/development.md) | Project layout, tests, contributing |
| [Troubleshooting](docs/guides/troubleshooting.md) | Common errors |

Copy-paste templates and badge previews: [`examples/`](examples/README.md) (`config/` + `workflows/` are copyable; `badges/` is preview-only).

## License

See [LICENSE](LICENSE).
