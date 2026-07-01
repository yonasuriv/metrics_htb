# Getting started

HTB Ctrl terminal commands let you interact with Hack The Box from your shell: list machines, submit flags, start/stop/reset labs, and check stats — without opening a browser.

> [!NOTE]
> **About Kitty:** [Kitty](https://sw.kovidgoyal.net/kitty/) is a GPU-accelerated terminal that supports inline images. HTB Ctrl uses `kitten icat` to render machine avatars. **Don't have Kitty? No problem** — everything works fine; you just won't see avatar images.

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.11+ |
| **HTB token** | [Create an app token](https://app.hackthebox.com/account-settings) → API Key → Create App Token |
| **Terminal** | Any terminal (Kitty recommended for images) |
| **Dependencies** | Installed automatically on first `htbctrl` run |

## Install

From the **htb-ctrl** repo root (or after `bash scripts/install.sh`):

```bash
htbctrl --help          # bootstraps .venv on first run
htbctrl auth --token YOUR_TOKEN
htbctrl machines
```

## Authenticate

### 1. Get your HTB token

Go to [HTB Settings → API Key](https://app.hackthebox.com/account-settings) and create a new App Token. Copy the generated token (shown only once).

### 2. Save credentials

```bash
htbctrl auth --token YOUR_TOKEN_HERE
```

> [!IMPORTANT]
> Your token is stored in `~/.config/htb-ctrl/cli/config.json` with permissions `600` (owner read/write only).

## First commands

```bash
htbctrl                  # Show help menu
htbctrl --help           # Same
htbctrl machines         # List active machines
htbctrl profile          # Your stats
```

## Next steps

- [Usage](cli-usage.md) — machines, flags, lab control, profile, cache
- [Configuration](configuration.md) — config files, cache, avatar sizes
- [Development](cli-development.md) — architecture and contributing
