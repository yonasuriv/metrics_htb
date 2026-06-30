<div align="center">

<img src="assets/00.png" alt="HTB CLI Banner" style="border-radius: 15px; max-width: 100%;">

</div>

# HTB CLI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)
![API](https://img.shields.io/badge/HTB_API-v4-9FEF00.svg?style=flat&logo=hackthebox&logoColor=white)
![Terminal](https://img.shields.io/badge/Terminal-Kitty%20%7C%20Any-FF6B6B.svg?style=flat&logo=windowsterminal&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00C853.svg?style=flat)

**Hack The Box from your terminal — no browser required**

</div>

---

## Overview

A fast CLI for Hack The Box: list machines, submit flags, spawn/stop/reset labs, and view profile stats. Built with Python, Rich UI, and optional Kitty terminal inline avatars.

> [!NOTE]
> **Kitty optional:** [Kitty](https://sw.kovidgoyal.net/kitty/) enables inline machine avatars via `kitten icat`. Everything else works in any terminal.

## Quick start

```bash
pip install -r src/htb_cli/requirements.txt
python3 src/htb_cli/htbcli.py auth --token YOUR_TOKEN
python3 src/htb_cli/htbcli.py machines
```

Get a token at [HTB Settings → API Key](https://app.hackthebox.com/account-settings).

## Documentation

Full guides with screenshots live under [`docs/guides/cli/`](../../docs/guides/cli/):

| Guide | Description |
|-------|-------------|
| [Getting started](../../docs/guides/cli/getting-started.md) | Install, authenticate, first commands |
| [Usage](../../docs/guides/cli/usage.md) | Machines, flags, lab control, profile, cache |
| [Configuration](../../docs/guides/cli/configuration.md) | Config files, cache, avatar sizes |
| [Development](../../docs/guides/cli/development.md) | Architecture, stack, contributing |
| [Troubleshooting](../../docs/guides/cli/troubleshooting.md) | Common errors |

## License

MIT — see [LICENSE](../../LICENSE).
