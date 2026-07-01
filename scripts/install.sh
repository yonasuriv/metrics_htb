#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/yonasuriv/htb-ctrl.git"
PREFIX=""
BIN_DIR="${HOME}/.local/bin"
SKIP_CLONE=0
SKIP_SETUP=0
ALIAS=""
FORCE=0

usage() {
  cat <<'EOF'
Usage: install.sh [options]

Options:
  --prefix PATH     Install directory (default: $HOME/.local/opt/htb-ctrl or $HOME/Tools/htb-ctrl)
  --bin-dir PATH    Symlink target (default: $HOME/.local/bin)
  --repo URL        Git remote (default: upstream htb-ctrl)
  --skip-clone      Use existing checkout at --prefix
  --skip-setup      Skip bootstrap trigger after install
  --alias NAME      Append shell alias (e.g. htbcli)
  --force           Re-clone into prefix if it exists
  -h, --help        Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prefix) PREFIX="$2"; shift 2 ;;
    --bin-dir) BIN_DIR="$2"; shift 2 ;;
    --repo) REPO_URL="$2"; shift 2 ;;
    --skip-clone) SKIP_CLONE=1; shift ;;
    --skip-setup) SKIP_SETUP=1; shift ;;
    --alias) ALIAS="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$PREFIX" ]]; then
  if [[ -w "${HOME}/.local/opt" ]] || mkdir -p "${HOME}/.local/opt" 2>/dev/null; then
    PREFIX="${HOME}/.local/opt/htb-ctrl"
  else
    PREFIX="${HOME}/Tools/htb-ctrl"
  fi
fi

mkdir -p "$(dirname "$PREFIX")" "$BIN_DIR"

if [[ "$SKIP_CLONE" -eq 0 ]]; then
  if [[ -d "$PREFIX/.git" ]]; then
    if [[ "$FORCE" -eq 1 ]]; then
      rm -rf "$PREFIX"
      git clone "$REPO_URL" "$PREFIX"
    else
      git -C "$PREFIX" pull --ff-only
    fi
  elif [[ -d "$PREFIX" ]]; then
    echo "[E] $PREFIX exists and is not a git repo. Use --force or --skip-clone." >&2
    exit 1
  else
    git clone "$REPO_URL" "$PREFIX"
  fi
fi

ln -sf "$PREFIX/htbctrl.py" "$BIN_DIR/htbctrl"
chmod +x "$PREFIX/htbctrl.py" 2>/dev/null || true

if [[ -n "$ALIAS" ]]; then
  RC="${HOME}/.$(basename "${SHELL}")rc"
  if ! grep -q "alias ${ALIAS}=" "$RC" 2>/dev/null; then
    printf '\nalias %s="htbctrl"\n' "$ALIAS" >> "$RC"
    echo "[+] Added alias ${ALIAS} to ${RC}"
  fi
fi

if [[ "$SKIP_SETUP" -eq 0 ]]; then
  echo "[*] Bootstrapping environment (first run may take a minute)..." >&2
  unset HTBCTRL_SKIP_BOOTSTRAP
  "$BIN_DIR/htbctrl" --help >/dev/null
fi

echo "[+] HTB Ctrl installed"
echo "    Prefix:  $PREFIX"
echo "    Binary:  $BIN_DIR/htbctrl"
echo "    Docs:    $PREFIX/docs/guides/README.md"
