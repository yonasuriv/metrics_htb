# Configuration

## Config files

| File | Purpose |
|------|---------|
| `~/.config/htbcli/config.json` | API token (chmod 600) |
| `~/.config/htbcli/cache.json` | Machine list cache |

Set your token once with:

```bash
python3 src/htb_cli/htbcli.py auth --token YOUR_TOKEN_HERE
```

See [Getting started → Authenticate](getting-started.md#authenticate).

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
