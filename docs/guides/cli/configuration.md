# Configuration

## Config files

| File | Purpose |
|------|---------|
| `htb-cli.yml` | Optional repo-root YAML (token keys) |
| `htb-metrics.yml` | Fallback YAML token keys (shared with metrics) |
| `.env` | Optional env vars (`HTB_API_TOKEN`, etc.) |
| `~/.config/htbm/cli/config.json` | Saved token from `auth --token` (chmod 600) |
| `~/.config/htbm/cli/cache.json` | Machine list cache |

Example files: [`examples/config/`](../../examples/config/)

## Token priority

| Mode | Order |
|------|--------|
| Default | **CLI flags** (`--api-token`, `--bearer`) → env vars → `htb-cli.yml` → `htb-metrics.yml` → `~/.config/htbm/cli/config.json` |
| `--from-env` | **env vars** (from `.env`) → CLI flags → YAML files → saved config |

Set your token once with any of:

```bash
python htbm.py cli auth --token YOUR_TOKEN_HERE
cp examples/config/.env.example .env          # HTB_API_TOKEN=…
cp examples/config/htb-cli.yml.example htb-cli.yml
```

See [Getting started → Authenticate](getting-started.md#authenticate).

## Global CLI flags

Forwarded through `python htbm.py cli …`:

| Flag | Description |
|------|-------------|
| `--from-env` | Load token from `.env` (env wins over CLI/YAML) |
| `--env-file` | Dotenv path (default `.env`) |
| `--config` | CLI YAML path (default `htb-cli.yml`) |
| `--metrics-config` | Fallback metrics YAML (default `htb-metrics.yml`) |
| `--api-token` | HTB app API token |
| `--bearer` | HTB bearer token |

`auth --token` still writes to `~/.config/htbm/cli/config.json` and works without any YAML or `.env`.

## Cache

HTB CLI caches machine lists locally for faster responses:

| Dataset | TTL |
|---------|-----|
| Active machines | 1 hour |
| Retired machines | 24 hours |

Use `--refresh` on `machines` to bypass cache, or run `cache --clear` to wipe it.

## Avatar image size

Adjust avatar size by editing the constants at the top of `src/htb_cli/htbcli.py`:

```python
MACHINE_INFO_IMG_COLS = 31   # machine-info command
ACTIVE_IMG_COLS       = 26   # active command

# 25 = small | 31 = medium | 50 = large
```

Kitty terminal with `kitten icat` is required for inline avatar rendering. Other terminals show all data except images.

## See also

- [Usage](usage.md) — all commands
- [Development](development.md) — how caching and rendering work
