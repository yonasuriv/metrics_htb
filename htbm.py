#!/usr/bin/env python3
"""HTB Manager — unified entry point for metrics, CLI, and dashboard."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC = REPO_ROOT / "src"
HTBCLI = SRC / "htb_cli" / "htbcli.py"
DASHBOARD_DIR = SRC / "htb_dashboard"
DASHBOARD_INDEX = DASHBOARD_DIR / "index.html"

if SRC.is_dir() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _venv_bin(name: str) -> Path:
    if os.name == "nt":
        return REPO_ROOT / ".venv" / "Scripts" / name
    return REPO_ROOT / ".venv" / "bin" / name


def cmd_setup() -> None:
    venv_dir = REPO_ROOT / ".venv"
    print(f"[*] Creating virtual environment at {venv_dir}")
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True, cwd=REPO_ROOT)

    pip = _venv_bin("pip")
    print("[*] Installing requirements")
    subprocess.run([str(pip), "install", "-r", "requirements.txt"], check=True, cwd=REPO_ROOT)

    playwright = _venv_bin("playwright")
    print("[*] Installing Playwright Chromium")
    subprocess.run([str(playwright), "install", "chromium"], check=True, cwd=REPO_ROOT)

    activate = REPO_ROOT / ".venv" / "bin" / "activate"
    print("\n[+] Setup complete.")
    print(f"    Activate: source {activate}")


def cmd_cli(forward_args: list[str]) -> None:
    cmd = [sys.executable, str(HTBCLI), *forward_args]
    raise SystemExit(subprocess.run(cmd, cwd=REPO_ROOT).returncode)


def cmd_metrics(mode: str, forward_args: list[str]) -> None:
    from htb_metrics.cli import pull_main, main as generate_main

    if mode == "pull":
        pull_main(forward_args)
    else:
        generate_main(forward_args)


def _open_browser(url: str) -> None:
    webbrowser.open(url)


def cmd_dashboard(serve: bool, port: int) -> None:
    if not DASHBOARD_INDEX.is_file():
        print(f"[E] Dashboard not found: {DASHBOARD_INDEX}", file=sys.stderr)
        raise SystemExit(1)

    if serve:
        os.chdir(DASHBOARD_DIR)

        class Handler(SimpleHTTPRequestHandler):
            def log_message(self, format: str, *args) -> None:  # noqa: A003
                return

        server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        url = f"http://127.0.0.1:{port}/"
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print(f"[*] Dashboard serving at {url}")
        print("    Press Ctrl+C to stop.")
        _open_browser(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Stopping server.")
            server.shutdown()
    else:
        url = DASHBOARD_INDEX.resolve().as_uri()
        print(f"[*] Opening dashboard in offline mode: {url}")
        print("    Use the file picker if the spreadsheet does not load automatically.")
        _open_browser(url)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="htbm",
        description="HTB Manager — metrics badges, terminal CLI, and browser dashboard",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("setup", help="Create venv, install deps, and install Playwright Chromium")

    cli_parser = sub.add_parser("cli", help="Run the HTB terminal CLI (htbcli)")
    cli_parser.add_argument("cli_args", nargs=argparse.REMAINDER, help="Arguments passed to htbcli")

    metrics_parser = sub.add_parser("metrics", help="Fetch HTB profile data and/or generate badges")
    metrics_group = metrics_parser.add_mutually_exclusive_group(required=True)
    metrics_group.add_argument("--pull", action="store_true", help="Fetch API data to user/<id>/data JSON files only")
    metrics_group.add_argument(
        "--generate",
        action="store_true",
        help="Full workflow: fetch data, build dataset, render badge PNG/SVG",
    )
    metrics_parser.add_argument(
        "metrics_args",
        nargs=argparse.REMAINDER,
        help="Arguments forwarded to htb_metrics config (e.g. -p, -t, --from-env)",
    )

    dash_parser = sub.add_parser("dashboard", help="Open the HTB machines cheat sheet dashboard")
    dash_parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve dashboard over HTTP instead of opening file:// offline mode",
    )
    dash_parser.add_argument("--port", type=int, default=8080, help="Port for --serve (default: 8080)")

    return parser


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "setup":
        cmd_setup()
    elif args.command == "cli":
        forward = args.cli_args
        if forward and forward[0] == "--":
            forward = forward[1:]
        cmd_cli(forward)
    elif args.command == "metrics":
        forward = args.metrics_args
        if forward and forward[0] == "--":
            forward = forward[1:]
        mode = "pull" if args.pull else "generate"
        cmd_metrics(mode, forward)
    elif args.command == "dashboard":
        cmd_dashboard(serve=args.serve, port=args.port)
    else:
        parser.print_help()
        raise SystemExit(2)


if __name__ == "__main__":
    main()
