# Configuration

Single reference for config files, env vars, and resolution priority across CLI, metrics, badges, and dashboard.

## Config files

| File | Purpose |
|------|---------|
| `~/.config/htb-ctrl/config.yml` | User SSOT (recommended) |
| `htb-ctrl.yml` | Repo-local override (dev / Actions checkout) |
| `.env` | Local secrets and profile ID |
| `htb-cli.yml` | Legacy CLI token YAML |
| `htb-metrics.yml` | Legacy metrics YAML |
| `~/.config/htb-ctrl/cli/config.json` | Token saved by `htbctrl auth --token` (chmod 600) |
| `~/.config/htb-ctrl/cli/cache.json` | CLI machine-list cache (runtime only) |

Examples: [`examples/config/`](../../examples/config/)

### Unified YAML (`htb-ctrl.yml`)

Copy [`examples/config/htb-ctrl.yml.example`](../../examples/config/htb-ctrl.yml.example):

```yaml
profile_id: 000000
auth:
  # api_token: ...
metrics:
  template: classic
  cache_ttl: 3600
cli:
  hide_banner: false
  machine_info_img_cols: 31
  active_img_cols: 26
dashboard:
  default_port: 8080
```

## Resolution priority

| Mode | Order |
|------|--------|
| Default | **CLI flags** → env vars → repo `htb-ctrl.yml` → `~/.config/htb-ctrl/config.yml` → legacy `htb-cli.yml` / `htb-metrics.yml` → `config.json` → defaults |
| `--from-env` | **env vars** (from `.env`) → CLI flags → YAML files → saved config |

## Global CLI flags

Available on every `htbctrl` command:

| Flag | Description |
|------|-------------|
| `--from-env` | Load from `.env` (env wins over CLI/YAML) |
| `--env-file` | Dotenv path (default `.env`) |
| `--config` | Legacy CLI YAML (default `htb-cli.yml`) |
| `--metrics-config` | Legacy metrics YAML (default `htb-metrics.yml`) |
| `--api-token` | HTB app API token |
| `--bearer` | HTB bearer token |
| `--hide-banner` | Suppress startup banner on help |

## Environment variables

| Variable | Used by | Description |
|----------|---------|-------------|
| `HTB_PROFILE_ID` | Metrics/badges | 6-digit profile ID |
| `HTB_API_TOKEN` | All | App API token |
| `HTB_TOKEN` | All | Token alias |
| `HTB_BEARER` | All | Bearer alias |
| `HTB_TEMPLATE` | Metrics | Badge template name |
| `HTB_OUTPUT_DIR` | Metrics | Badge output dir |
| `HTB_CACHE_DIR` | Metrics | Data cache dir |
| `HTB_CACHE_TTL` | Metrics | Cache TTL (seconds) |
| `HTB_NO_CACHE` | Metrics | Disable cache |
| `HTB_HIDE_IF_NULL` | Metrics | Hide empty badge fields |
| `HTBCTRL_SKIP_BOOTSTRAP` | Launcher | Skip venv bootstrap |

## Authentication

```bash
htbctrl auth --token YOUR_TOKEN
cp examples/config/.env.example .env
cp examples/config/htb-ctrl.yml.example htb-ctrl.yml
```

Token priority (default): `--api-token` / `--bearer` → env → YAML → `config.json`.

## Metrics & badges flags

Forwarded after subcommand:

```bash
htbctrl metrics pull -p 780424
htbctrl badges generate -p 780424 -t classic --from-env
```

| Flag | Description |
|------|-------------|
| `-p`, `--profile` | Profile ID |
| `-t`, `--template` | Template name |
| `-o`, `--output-dir` | Badge output directory |
| `--no-cache` | Disable API cache |

## CLI cache & avatars

| Dataset | TTL |
|---------|-----|
| Active machines | 1 hour |
| Retired machines | 24 hours |

Avatar column widths (`cli` section in `htb-ctrl.yml` or `src/ctrl_cli/cache.py` constants). Kitty + `kitten icat` required for inline images.

## User output layout

```
user/
└── 780424/
    ├── data/      # cached HTB API JSON
    └── badges/    # generated PNG/SVG
```

## See also

- [Installation](installation.md)
- [CLI usage](cli-usage.md)
- [Badge templates](badge-templates.md)
