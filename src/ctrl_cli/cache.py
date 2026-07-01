from __future__ import annotations

import json
import time

import typer

from ctrl_cli.config import CACHE_FILE, CONFIG_DIR, CONFIG_FILE
from ctrl_cli.ui import VERSION, console
BASE_URL = "https://labs.hackthebox.com/api/v4"
CACHE_TTL = {"active": 3600, "retired": 86400}
MACHINE_INFO_IMG_COLS = 31
ACTIVE_IMG_COLS = 26

_RUNTIME_TOKEN: str | None = None


def set_runtime_token(token: str | None) -> None:
    global _RUNTIME_TOKEN
    _RUNTIME_TOKEN = token


def get_runtime_token() -> str | None:
    return _RUNTIME_TOKEN


def load_config() -> dict:
    token = get_runtime_token()
    if token:
        return {"token": token}
    if not CONFIG_FILE.exists():
        console.print(
            "\n[bold red]No token configured.[/]\n"
            "  Run: [cyan bold]htbctrl auth --token YOUR_TOKEN[/]\n"
            "  Or set HTB_API_TOKEN in .env / htb-cli.yml / htb-metrics.yml\n"
            "  Get token at: HTB → Settings → API Key → Create App Token\n"
        )
        raise typer.Exit(1)
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError:
        console.print("[bold red]Config corrupted.[/] Run htbctrl auth again.")
        raise typer.Exit(1)

def save_config(data: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)
    CONFIG_FILE.chmod(0o600)

def get_headers() -> dict:
    return {
        "Authorization": f"Bearer {load_config()['token']}",
        "Content-Type":  "application/json",
        "Accept":        "application/json",
        "User-Agent":    f"HTB-CTRL/{VERSION}",
    }

def cache_load(key: str) -> list | None:
    if not CACHE_FILE.exists():
        return None
    try:
        with open(CACHE_FILE) as f:
            cache = json.load(f)
        entry = cache.get(key, {})
        age   = time.time() - entry.get("ts", 0)
        ttl   = CACHE_TTL.get(key, 3600)
        if age < ttl and entry.get("data"):
            return entry["data"]
    except Exception:
        pass
    return None

def cache_save(key: str, data: list):
    cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                cache = json.load(f)
        except Exception:
            pass
    cache[key] = {"data": data, "ts": time.time()}
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def cache_clear():
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()

