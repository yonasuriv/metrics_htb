# Getting started

<div align="center">

<img src="../../../src/htb_cli/assets/00.png" alt="HTB CLI Banner" style="border-radius: 15px; max-width: 100%;">

</div>

HTB CLI is a fast, full-featured command-line tool for interacting with Hack The Box directly from your terminal. List machines, submit flags, start/stop/reset labs, and check your stats — all without opening a browser.

> [!NOTE]
> **About Kitty:** [Kitty](https://sw.kovidgoyal.net/kitty/) is a GPU-accelerated terminal that supports inline images. HTB CLI uses `kitten icat` to render machine avatars. **Don't have Kitty? No problem** — everything works fine; you just won't see avatar images.

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10+ |
| **HTB token** | [Create an app token](https://app.hackthebox.com/account-settings) → API Key → Create App Token |
| **Terminal** | Any terminal (Kitty recommended for images) |
| **Dependencies** | `typer`, `requests`, `rich` |

## Install

From the **metrics-htb** repo root:

```bash
git clone https://github.com/yonasuriv/metrics-htb.git
cd metrics-htb
pip install -r src/htb_cli/requirements.txt
```

Optional — make it executable and add an alias:

```bash
chmod +x src/htb_cli/htbcli.py
echo 'alias htbcli="python3 ~/metrics-htb/src/htb_cli/htbcli.py"' >> ~/.zshrc
source ~/.zshrc
```

## Authenticate

### 1. Get your HTB token

Go to [HTB Settings → API Key](https://app.hackthebox.com/account-settings) and create a new App Token:

![create-token](../../../src/htb_cli/assets/02.jpg)

Copy the generated token (shown only once):

![copy-token](../../../src/htb_cli/assets/03.jpg)

### 2. Save credentials

```bash
python3 src/htb_cli/htbcli.py auth --token YOUR_TOKEN_HERE
```

![auth](../../../src/htb_cli/assets/04.jpg)

> [!IMPORTANT]
> Your token is stored in `~/.config/htbcli/config.json` with permissions `600` (owner read/write only).

## First commands

```bash
python3 src/htb_cli/htbcli.py              # Show help menu
python3 src/htb_cli/htbcli.py --help       # Same
python3 src/htb_cli/htbcli.py machines     # List active machines
python3 src/htb_cli/htbcli.py profile      # Your stats
```

![htbcli](../../../src/htb_cli/assets/01.jpg)

## Next steps

- [Usage](usage.md) — machines, flags, lab control, profile, cache
- [Configuration](configuration.md) — config files, cache, avatar sizes
- [Development](development.md) — architecture and contributing
