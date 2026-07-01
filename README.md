<div align="center" id="madewithlua">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset=".github/assets/logo-light.png">
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-dark.png">
    <img src=".github/assets/logo-dark.png" alt="HTB Metrics">
  </picture>
</div>

---

<div align="center">
  <p>Your Hack The Box data, wherever you want it:
  </p> 
  <p>
    <b>Terminal</b>, <b>Spreadsheets</b>, <b>Browser</b>, or <b>GitHub Profile Badges</b> updated automatically via GitHub Actions.
    </p>
</div>

---

<br>
<div align="center">
  
  ![Terminal](https://img.shields.io/badge/Terminal-Any-FF6B6B.svg?style=flat&logo=windowsterminal&logoColor=white)
  ![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)
  ![API](https://img.shields.io/badge/HTB_API-v4%20%7C%20v5-9FEF00.svg?style=flat&logo=hackthebox&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-00C853.svg?style=flat)
  
</div>

## Features

- **CLI**
  - A fast CLI for Hack The Box: list machines, submit flags, spawn/stop/reset labs, and view profile stats.
  - Built with Python, Rich UI, and optional Kitty terminal inline avatars.

- **Badges**
  - Auto-generated profile badges for your GitHub README
  - **12 templates** — classic, terminal, GitHub-style cards, minimal badge, and more
  - **Public + optional auth** — works with a public profile; app token unlocks extra API data
  - **No fork required** — copy a workflow template into your profile repo
 
- **Dashboard**
  - An interactive browser dashboard to visualize every Hack The Box machine you've completed
  - Searchable table of pwned machines with techniques, difficulty, OS, dates, and writeup links
  - Excel-driven updates.

## Quick start

Clone the repository and run setup:

```bash
git clone https://github.com/yonasuriv/htb-ctrl.git && cd htb-ctrl
python htbctrl.py setup --init
source .venv/bin/activate   # then edit .env with your HTB_PROFILE_ID
```

`htbctrl.py` is the unified entry point for all three components.

| Command | Description |
|---------|-------------|
| `python htbctrl.py setup` | Create venv, install deps, install Playwright Chromium |
| `python htbctrl.py setup --init` | Setup plus init (`.env` from example, `~/.config/htb-ctrl/cli`) |
| `python htbctrl.py init` | Copy `.env` example and create config dir (requires `.venv`) |
| `python htbctrl.py cli …` | HTB terminal CLI (same as `src/htb_cli/htbcli.py`) |
| `python htbctrl.py metrics --pull …` | Fetch HTB API data to `user/<id>/data/` JSON files |
| `python htbctrl.py metrics --generate …` | Full badge workflow → `user/<id>/badges/` |
| `python htbctrl.py dashboard` | Open dashboard offline (`file://` + file picker) |
| `python htbctrl.py dashboard --serve` | Serve dashboard on http://127.0.0.1:8080 |
| `python htbctrl.py dashboard --new-sheet` | Create header-only `htb_machines.xlsx` at repo root |

User output layout:

```
user/
└── 780424/
    ├── data/      # cached HTB API JSON (replaces .cache/780424)
    └── badges/    # generated PNG/SVG (replaces output/)
```

---

### CLI

```bash
python htbctrl.py cli auth --token YOUR_TOKEN
python htbctrl.py cli machines
```

> [!NOTE]
> **Kitty optional:** [Kitty](https://sw.kovidgoyal.net/kitty/) enables inline machine avatars via `kitten icat`. Everything else works in any terminal.

> Get a token at [HTB Settings → API Key](https://app.hackthebox.com/account-settings).

---

### Badges

```bash
python htbctrl.py metrics --pull -p PROFILE_ID
python htbctrl.py metrics --generate -p PROFILE_ID
python htbctrl.py metrics --generate --from-env
```

> For GitHub Actions: [see here](docs/guides/badge/getting-started.md#github-actions-no-fork).

---

### Dashboard

```bash
python htbctrl.py dashboard --new-sheet
python htbctrl.py dashboard --serve
```

Edit `htb_machines.xlsx` at the repo root as you pwn new boxes; reload the page to refresh. Sample format: [`examples/sheets/htb_machines_example.xlsx`](examples/sheets/htb_machines_example.xlsx).

## Documentation

#### Badges (`src/htb_metrics`)

| Guide | Description |
|-------|-------------|
| [Getting started](docs/guides/badge/getting-started.md) | Install, first badge, GitHub Actions |
| [Configuration](docs/guides/badge/configuration.md) | CLI, env, YAML, secrets, cache |
| [GitHub Actions](docs/guides/badge/github-actions.md) | Workflow templates in `examples/workflows/` |
| [Templates](docs/guides/badge/templates.md) | Placeholders and template list |
| [Data sources](docs/guides/badge/data-sources.md) | HTB API endpoints |
| [Development](docs/guides/badge/development.md) | Project layout, tests, contributing |
| [Troubleshooting](docs/guides/badge/troubleshooting.md) | Common errors |

#### CLI (`src/htb_cli`)

| Guide | Description |
|-------|-------------|
| [Getting started](docs/guides/cli/getting-started.md) | Install, authenticate, first commands |
| [Usage](docs/guides/cli/usage.md) | Machines, flags, lab control, profile, cache |
| [Configuration](docs/guides/cli/configuration.md) | Config files, cache, avatar sizes |
| [Development](docs/guides/cli/development.md) | Architecture, stack, contributing |
| [Troubleshooting](docs/guides/cli/troubleshooting.md) | Common errors |

#### Dashboard (`src/htb_dashboard`)

| Guide | Description |
|-------|-------------|
| [Getting started](docs/guides/dashboard/getting-started.md) | Setup and project layout |
| [Features](docs/guides/dashboard/features.md) | Table, badges, DataTables, Excel loading |
| [Customization](docs/guides/dashboard/customization.md) | Add techniques and tweak styles |
| [Development](docs/guides/dashboard/development.md) | Tech stack and data flow |

### Credits

This work was heavily inspired by the following authors:
- [Lowlighter](https://github.com/lowlighter)
- [D1se0](https://github.com/d1se0)
- [K-4yser](https://github.com/k-4yser)

## License

MIT — see [LICENSE](/LICENSE).
