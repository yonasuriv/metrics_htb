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

- **Metrics**
  - Get detailed data of all your activity in hack the box; paths, tracks, ranks, everything

- **Badges**
  - Auto-generated profile badges for your GitHub README
  - 12 templates: classic, terminal, GitHub-style cards, minimal badge, and more
  - Public + optional auth: works with a public profile; app token unlocks extra API data
  - No fork required: copy a workflow template into your profile repo
 
- **Dashboard**
  - An interactive browser dashboard to visualize every Hack The Box machine you've completed
  - Searchable table of pwned machines with techniques, difficulty, OS, dates, and writeup links
  - Excel-driven updates.

## Quick start

### Install anywhere

```bash
bash scripts/install.sh
# or: curl -fsSL …/scripts/install.sh | bash
```

Manual equivalent:

```bash
mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"
git clone https://github.com/yonasuriv/htb-ctrl.git "$HOME/.local/opt/htb-ctrl"
ln -sf "$HOME/.local/opt/htb-ctrl/htbctrl.py" "$HOME/.local/bin/htbctrl"
htbctrl --help
```

First run bootstraps `.venv` and dependencies silently. See [Installation](docs/guides/installation.md).

### Development checkout

```bash
git clone https://github.com/yonasuriv/htb-ctrl.git && cd htb-ctrl
htbctrl --help
```

> Copy `examples/config/.env.example` to `.env` and set `HTB_PROFILE_ID`, or pass `-p` on metrics commands.

## Commands

| Command | Description |
|---------|-------------|
| `htbctrl man` | Full command and flag reference |
| `htbctrl auth --token …` | Save HTB API token |
| `htbctrl machines` | List/search machines |
| `htbctrl metrics pull …` | Fetch profile data to `user/<id>/data/` |
| `htbctrl badges generate …` | Full badge workflow → `user/<id>/badges/` |
| `htbctrl dashboard` | Open dashboard offline |
| `htbctrl dashboard --serve` | Serve on http://127.0.0.1:8080 |
| `htbctrl dashboard --new-sheet` | Create `htb_machines.xlsx` at repo root |

Global flags: `--from-env`, `--api-token`, `--bearer`, `--hide-banner`. See [Configuration](docs/guides/configuration.md).

User output layout:

```
user/
└── 780424/
    ├── data/      # cached HTB API JSON
    └── badges/    # generated PNG/SVG
```

### CLI

```bash
htbctrl auth --token YOUR_TOKEN
htbctrl machines
```

> [!NOTE]
> **Kitty optional:** [Kitty](https://sw.kovidgoyal.net/kitty/) enables inline machine avatars via `kitten icat`. Everything else works in any terminal.

> Get a token at [HTB Settings → API Key](https://app.hackthebox.com/account-settings).

### Badges

```bash
htbctrl metrics pull -p PROFILE_ID
htbctrl badges generate -p PROFILE_ID
htbctrl badges generate --from-env
```

> Set the workflow in your profile without forking: [Getting Started → GitHub Actions](docs/guides/badge-getting-started.md#github-actions-no-fork).

### Dashboard

```bash
htbctrl dashboard --new-sheet
htbctrl dashboard --serve
```

> Edit `htb_machines.xlsx` at the repo root as you pwn new boxes; reload the page to refresh.

## Documentation

Full guide index: **[docs/guides/README.md](docs/guides/README.md)**

| Area | Start here |
|------|------------|
| Install & bootstrap | [installation.md](docs/guides/installation.md) |
| Config (SSOT) | [configuration.md](docs/guides/configuration.md) |
| Terminal CLI | [cli-getting-started.md](docs/guides/cli-getting-started.md) |
| Badges | [badge-getting-started.md](docs/guides/badge-getting-started.md) |
| Dashboard | [dashboard-getting-started.md](docs/guides/dashboard-getting-started.md) |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](/LICENSE).

> This project is not affiliated with, endorsed by, or associated with [Hack The Box](https://www.hackthebox.com/).

## Credits

This work was heavily inspired by the following authors:

- [Lowlighter](https://github.com/lowlighter)
- [D1se0](https://github.com/d1se0)
- [K-4yser](https://github.com/k-4yser)