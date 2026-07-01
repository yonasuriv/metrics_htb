from __future__ import annotations

import fcntl
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VENV_DIR = REPO_ROOT / ".venv"
LOCK_FILE = VENV_DIR / ".bootstrap.lock"
DEPS_STAMP = VENV_DIR / ".deps_ok"


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def venv_pip() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"


def venv_playwright() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "playwright.exe"
    return VENV_DIR / "bin" / "playwright"


def should_bootstrap() -> bool:
    if os.environ.get("HTBCTRL_SKIP_BOOTSTRAP", "").strip().lower() in ("1", "true", "yes"):
        return False
    if os.environ.get("CI", "").strip().lower() in ("1", "true", "yes"):
        return False
    return True


def running_in_venv() -> bool:
    """True only when the active interpreter is the repo .venv (not system python)."""
    if not venv_python().is_file():
        return False
    try:
        return Path(sys.prefix).resolve() == VENV_DIR.resolve()
    except (OSError, ValueError):
        return False


def _with_lock(fn) -> None:
    VENV_DIR.mkdir(parents=True, exist_ok=True)
    with LOCK_FILE.open("w") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        fn()
        lock.flush()


def ensure_runtime(*, quiet: bool = True) -> None:
    """Create venv and install deps if missing (idempotent)."""

    def _run() -> None:
        if not venv_python().is_file():
            if not quiet:
                print(f"[*] Creating virtual environment at {VENV_DIR}", file=sys.stderr)
            subprocess.run(
                [sys.executable, "-m", "venv", str(VENV_DIR)],
                check=True,
                cwd=REPO_ROOT,
            )

        req = REPO_ROOT / "requirements.txt"
        req_mtime = req.stat().st_mtime if req.is_file() else 0
        stamp_mtime = DEPS_STAMP.stat().st_mtime if DEPS_STAMP.is_file() else 0

        if not DEPS_STAMP.is_file() or stamp_mtime < req_mtime:
            if not quiet:
                print("[*] Installing requirements", file=sys.stderr)
            subprocess.run(
                [str(venv_pip()), "install", "-r", "requirements.txt"],
                check=True,
                cwd=REPO_ROOT,
            )
            subprocess.run(
                [str(venv_pip()), "install", "-e", "."],
                check=True,
                cwd=REPO_ROOT,
            )
            pw = venv_playwright()
            if pw.is_file():
                if not quiet:
                    print("[*] Installing Playwright Chromium", file=sys.stderr)
                subprocess.run([str(pw), "install", "chromium"], check=True, cwd=REPO_ROOT)
            DEPS_STAMP.write_text("ok\n")

    _with_lock(_run)


def silent_init() -> None:
    """Ensure config dir, repo .env, and dashboard spreadsheet (no user-facing output)."""
    config_dir = Path.home() / ".config" / "htb-ctrl" / "cli"
    config_dir.mkdir(parents=True, exist_ok=True)

    env_dest = REPO_ROOT / ".env"
    env_example = REPO_ROOT / "examples" / "config" / ".env.example"
    if not env_dest.is_file() and env_example.is_file():
        shutil.copy2(env_example, env_dest)

    ensure_dashboard_sheet()


def ensure_dashboard_sheet() -> Path | None:
    """Create htb_machines.xlsx at repo root when missing."""
    from ctrl_dashboard.sheet import create_new_sheet, default_sheet_path

    dest = default_sheet_path(REPO_ROOT)
    if dest.is_file():
        return None
    try:
        return create_new_sheet(dest=dest, root=REPO_ROOT)
    except FileExistsError:
        return None
