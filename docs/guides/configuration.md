# Configuration

## Priority

| Mode | Order |
|------|--------|
| Default | **CLI flags** → env vars → `htb-metrics.yml` → defaults |
| `--from-env` | **env vars** (from `.env`) → CLI flags → `htb-metrics.yml` → defaults |

Example files: [`examples/config/`](../../examples/config/)

## CLI flags

| Flag | Description |
|------|-------------|
| `-p`, `--profile` | 6-digit HTB profile ID |
| `-t`, `--template` | Template name (default `classic`) |
| `-o`, `--output-dir` | Output directory (default `output`) |
| `--api-token` | HTB app API token |
| `--token` | HTB app token (alias) |
| `--bearer` | HTB bearer token (alias) |
| `--from-env` | Load settings from `.env` (env wins over CLI/yaml) |
| `--env-file` | Dotenv path (default `.env`) |
| `--config` | YAML config path (default `htb-metrics.yml`) |
| `--no-cache` | Disable API response cache |

## Environment variables

Copy [`examples/config/.env.example`](../../examples/config/.env.example) to `.env` at the repo root.

| Variable | Description | Default |
|----------|-------------|---------|
| `HTB_PROFILE_ID` | Profile ID | *(required)* |
| `HTB_API_TOKEN` | App token | — |
| `HTB_TOKEN` | App token alias | — |
| `HTB_BEARER` | Bearer token alias | — |
| `HTB_TEMPLATE` | Template name | `classic` |
| `HTB_OUTPUT_DIR` | Output dir | `output` |
| `HTB_CACHE_DIR` | Cache dir | `.cache` |
| `HTB_CACHE_TTL` | Cache TTL (seconds) | `3600` |
| `HTB_NO_CACHE` | Disable cache | `false` |
| `HTB_HIDE_IF_NULL` | Hide empty template fields | `true` |

Booleans accept: `true`/`false`, `1`/`0`, `yes`/`no`, `on`/`off`.

Token resolution (first match): `HTB_API_TOKEN` → `HTB_TOKEN` → `HTB_BEARER` → YAML `api_token`/`token`/`bearer`.

## YAML config

Copy [`examples/config/htb-metrics.yml.example`](../../examples/config/htb-metrics.yml.example) to `htb-metrics.yml`.

```yaml
profile_id: 000000
template: classic
output_dir: output
cache_ttl: 3600
hide_if_null: true
cache_dir: .cache
# api_token: optional
```

## Authentication

Auth-only HTB endpoints (machines catalog, tracks, team rankings) are **skipped** when no token is configured.

Provide one of:

- CLI: `--api-token`, `--token`, or `--bearer`
- Env: `HTB_API_TOKEN`, `HTB_TOKEN`, or `HTB_BEARER`
- YAML: `api_token`, `token`, or `bearer`

Tokens are sent as `Authorization: Bearer <token>`. Never commit `.env` or tokens.

## GitHub Actions secrets

In your profile repo (Settings → Secrets → Actions):

| Secret | Required |
|--------|----------|
| `HTB_PROFILE_ID` | Yes |
| `HTB_API_TOKEN` / `HTB_TOKEN` / `HTB_BEARER` | No (one is enough) |

## Cache

API responses cache under `.cache/{profile_id}/`:

| File | Purpose |
|------|---------|
| `profile.json` | Main profile |
| `*.json` | Secondary API responses |
| `avatar_b64.txt` | Avatar as data URI for SVG templates |

Set `HTB_NO_CACHE=true` or `--no-cache` to always fetch fresh data.

## Console script

After `pip install -e .`:

```bash
htb-metrics -p YOUR_PROFILE_ID -t classic
```

Same as `python generate.py`.
