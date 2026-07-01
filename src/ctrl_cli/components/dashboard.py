from __future__ import annotations

import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import typer

from ctrl_cli import bootstrap as boot

dashboard_app = typer.Typer(help="HTB machines cheat sheet dashboard")


class DashboardHandler(SimpleHTTPRequestHandler):
    dashboard_dir: Path = boot.REPO_ROOT / "src" / "ctrl_dashboard"
    repo_root: Path = boot.REPO_ROOT

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def translate_path(self, path: str) -> str:
        clean = path.split("?", 1)[0].split("#", 1)[0]
        rel = clean.lstrip("/")
        base = self.dashboard_dir.resolve()

        if rel in ("", "index.html"):
            target = (base / "index.html").resolve()
        elif rel == "htb_machines.xlsx":
            target = (self.repo_root / "htb_machines.xlsx").resolve()
        else:
            target = (base / rel).resolve()

        if target == base or base in target.parents:
            return str(target)
        return str(base / "index.html")


def _open_browser(url: str) -> None:
    webbrowser.open(url)


def _create_sheet(*, force: bool = False) -> Path:
    from ctrl_dashboard.sheet import create_new_sheet, default_sheet_path

    dest = default_sheet_path(boot.REPO_ROOT)
    if dest.exists():
        if not force:
            typer.echo(f"[E] Spreadsheet already exists: {dest}", err=True)
            raise typer.Exit(1)
        dest.unlink()
    created = create_new_sheet(dest=dest, root=boot.REPO_ROOT)
    typer.echo(f"[+] Created {created.relative_to(boot.REPO_ROOT)} (headers only)")
    return created


@dashboard_app.callback(invoke_without_command=True)
def dashboard_main(
    ctx: typer.Context,
    serve: bool = typer.Option(False, "--serve", help="Serve dashboard over HTTP"),
    port: int = typer.Option(8080, "--port", help="Port for --serve"),
    new_sheet: bool = typer.Option(
        False,
        "--new-sheet",
        help="Create header-only htb_machines.xlsx at the repo root",
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite existing spreadsheet with --new-sheet"),
):
    if ctx.invoked_subcommand is not None:
        return

    if new_sheet:
        _create_sheet(force=force)
        if not serve:
            raise typer.Exit(0)

    index = boot.REPO_ROOT / "src" / "ctrl_dashboard" / "index.html"
    if not index.is_file():
        typer.echo(f"[E] Dashboard not found: {index}", err=True)
        raise typer.Exit(1)

    sheet = boot.REPO_ROOT / "htb_machines.xlsx"

    if serve:
        DashboardHandler.dashboard_dir = index.parent
        DashboardHandler.repo_root = boot.REPO_ROOT
        server = ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler)
        url = f"http://127.0.0.1:{port}/"
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        typer.echo(f"[*] Dashboard serving at {url}")
        if sheet.is_file():
            typer.echo(f"    Spreadsheet: {sheet.name}")
        else:
            typer.echo("    No htb_machines.xlsx yet — run: htbctrl dashboard --new-sheet")
        typer.echo("    Press Ctrl+C to stop.")
        _open_browser(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            typer.echo("\n[*] Stopping server.")
            server.shutdown()
    else:
        url = index.resolve().as_uri()
        typer.echo(f"[*] Opening dashboard in offline mode: {url}")
        _open_browser(url)


def register(app: typer.Typer) -> None:
    app.add_typer(dashboard_app, name="dashboard")
