from __future__ import annotations

import typer
import requests
from rich.progress import Progress, SpinnerColumn, TextColumn

from ctrl_cli.cache import BASE_URL, cache_load, cache_save, get_headers
from ctrl_cli.ui import console


def _safe_json(r: requests.Response, silent: bool):
    if not r.content or not r.text.strip():
        return None
    try:
        return r.json()
    except Exception:
        if silent: return None
        console.print(f"[red]Error:[/] Response is not JSON (HTTP {r.status_code})")
        console.print(f"[dim]{r.text[:300]}[/dim]")
        raise typer.Exit(1)

def api_get(path: str, silent: bool = False):
    url = f"{BASE_URL}{path}"
    try:
        with Progress(SpinnerColumn(), TextColumn("[cyan]{task.description}"),
                      transient=True, console=console) as p:
            p.add_task("Loading...")
            r = requests.get(url, headers=get_headers(), timeout=20)
    except requests.exceptions.ConnectionError:
        if silent: return None
        console.print("[red]Error:[/] No connection. Check your network." + "\n")
        raise typer.Exit(1)
    except requests.exceptions.Timeout:
        if silent: return None
        console.print("[red]Error:[/] Timeout — HTB API not responding." + "\n")
        raise typer.Exit(1)

    if r.status_code == 401:
        console.print("\n[red]Error:[/] Invalid or expired token." + "\n")
        raise typer.Exit(1)
    if r.status_code == 429:
        if silent: return None
        console.print("[yellow]Warning:[/] Rate limit reached. Wait a few seconds." + "\n")
        raise typer.Exit(1)
    if r.status_code in (403, 404, 405, 422):
        if silent: return None
        data = _safe_json(r, silent=True)
        msg  = (data or {}).get("message", "") if isinstance(data, dict) else ""
        console.print(f"[red]Error {r.status_code}:[/]" + (f" {msg}" if msg else f" {path}"))
        raise typer.Exit(1)
    if not r.ok:
        if silent: return None
        console.print(f"[red]Error HTTP {r.status_code}[/]")
        raise typer.Exit(1)

    return _safe_json(r, silent)

def api_post(path: str, payload: dict, silent: bool = False):
    url = f"{BASE_URL}{path}"
    try:
        with Progress(SpinnerColumn(), TextColumn("[cyan]{task.description}"),
                      transient=True, console=console) as p:
            p.add_task("Sending...")
            r = requests.post(url, headers=get_headers(), json=payload, timeout=20)
    except requests.exceptions.ConnectionError:
        if silent: return None
        console.print("[red]Error:[/] No connection.")
        raise typer.Exit(1)

    if r.status_code == 401:
        console.print("[red]Error:[/] Invalid or expired token.")
        raise typer.Exit(1)

    data = _safe_json(r, silent=True)
    if not r.ok and not silent:
        msg = (data or {}).get("message", (data or {}).get("error", "")) if isinstance(data, dict) else ""
        console.print(f"[red]Error {r.status_code}:[/]" + (f" {msg}" if msg else ""))
    return data

def api_get_all_pages(base_path: str, per_page: int = 100) -> list:
    all_items: list = []
    page = 1

    while True:
        sep_char = "&" if "?" in base_path else "?"
        data     = api_get(f"{base_path}{sep_char}per_page={per_page}&page={page}",
                           silent=(page > 1))
        if data is None:
            break

        if isinstance(data, list):
            items     = data
            last_page = page if len(items) < per_page else page + 1
            curr_page = page
        elif isinstance(data, dict):
            items     = (data.get("data") or data.get("machines") or
                         data.get("items") or [])
            meta      = data.get("meta") or {}
            last_page = int(meta.get("last_page",  1))
            curr_page = int(meta.get("current_page", page))
        else:
            break

        if not isinstance(items, list) or not items:
            break

        all_items.extend(items)

        if curr_page >= last_page: break
        if len(items) < per_page:  break
        if page >= 30:             break

        page += 1

    return all_items

def fetch_machines(retired: bool, force: bool = False) -> list:
    key = "retired" if retired else "active"
    if not force:
        cached = cache_load(key)
        if cached:
            return cached
    label    = "retired" if retired else "active"
    endpoint = "/machine/list/retired/paginated" if retired else "/machine/paginated"
    data = api_get_all_pages(endpoint)
    if data:
        cache_save(key, data)
    return data

