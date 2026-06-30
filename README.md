# HTB Metrics

Auto-generated **Hack The Box profile badges** for your GitHub README — legacy rank, experience level, season league, flags, and more. Updated daily via GitHub Actions.

![HTB Metrics classic badge](https://github.com/user-attachments/assets/b7ad88f4-0ca5-4721-95a2-d125ab780dcf)

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

See [Template placeholders](docs/guides/templates.md) for all `$fields$`.

## Quick start

```bash
git clone https://github.com/yonasuriv/metrics-htb.git && cd metrics-htb
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && playwright install chromium
cp refs/config/.env.example .env   # set HTB_PROFILE_ID
python generate.py --from-env
```

For GitHub Actions (no fork): [Getting started → GitHub Actions](docs/guides/getting-started.md#github-actions-no-fork).

## Documentation

| Guide | Description |
|-------|-------------|
| [Getting started](docs/guides/getting-started.md) | Install, first badge, GitHub Actions |
| [Configuration](docs/guides/configuration.md) | CLI, env, YAML, secrets, cache |
| [GitHub Actions](docs/guides/github-actions.md) | Workflow templates in `refs/workflows/` |
| [Templates](docs/guides/templates.md) | Placeholders and template list |
| [Data sources](docs/guides/data-sources.md) | HTB API endpoints |
| [Development](docs/guides/development.md) | Project layout, tests, contributing |
| [Troubleshooting](docs/guides/troubleshooting.md) | Common errors |

Reference files (copy, do not run from this repo): [`refs/`](refs/README.md)

## License

See [LICENSE](LICENSE).
