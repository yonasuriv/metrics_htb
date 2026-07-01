# Installation

HTB Ctrl bootstraps its own virtual environment on first run. Manual `setup` / `init` are no longer required.

## Recommended: install script

```bash
curl -fsSL https://raw.githubusercontent.com/yonasuriv/htb-ctrl/main/scripts/install.sh | bash
```

Or from a local checkout:

```bash
bash scripts/install.sh
```

Defaults:

| Path | Purpose |
|------|---------|
| `$HOME/.local/opt/htb-ctrl` | Install prefix (falls back to `$HOME/Tools/htb-ctrl`) |
| `$HOME/.local/bin/htbctrl` | Symlink to launcher |

Options: `--prefix`, `--bin-dir`, `--skip-clone`, `--skip-setup`, `--alias NAME`, `--force`.

## Manual install

```bash
mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"
git clone https://github.com/yonasuriv/htb-ctrl.git "$HOME/.local/opt/htb-ctrl"
ln -sf "$HOME/.local/opt/htb-ctrl/htbctrl.py" "$HOME/.local/bin/htbctrl"
htbctrl --help   # triggers silent venv bootstrap
```

## Development checkout

```bash
git clone https://github.com/yonasuriv/htb-ctrl.git && cd htb-ctrl
htbctrl --help
```

First launch creates `.venv`, installs `requirements.txt`, and runs Playwright Chromium setup once.

## CI / tests

Set `HTBCTRL_SKIP_BOOTSTRAP=1` (or `CI=true`) to skip venv re-exec.

## See also

- [Configuration](configuration.md) — auth token and profile setup after install
