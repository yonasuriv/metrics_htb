from __future__ import annotations

import io
import os
import re
import subprocess
import sys
from pathlib import Path

from ctrl_config.version import project_version
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table

VERSION = project_version()

BANNER_FILE = Path(__file__).resolve().parent / "components" / "__banner__"
console = Console()

DIFF_COLORS = {"Easy": "green", "Medium": "yellow", "Hard": "red", "Insane": "bright_red"}

def _kitty_available() -> bool:
    """Check if we're running inside Kitty with kitten available."""
    import shutil
    return (
        bool(os.environ.get("KITTY_WINDOW_ID") or
             os.environ.get("TERM", "").startswith("xterm-kitty"))
        and shutil.which("kitten") is not None
    )

def _img_bytes(url: str, headers: dict | None = None):
    """Download image bytes, return None if not a valid image."""
    try:
        r = requests.get(url, timeout=8, headers=headers or {})
        if r.ok and (
            r.content[:4] in (b"\x89PNG", b"GIF8")
            or r.content[:3] == b"\xff\xd8\xff"
        ):
            return r.content
    except Exception:
        pass
    return None

def _query_cursor_y():
    """Get current cursor row (1-based) using ANSI DSR escape."""
    try:
        fd = sys.stdin.fileno()
        if not os.isatty(fd):
            return None
        import termios, tty, select
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            os.write(sys.stdout.fileno(), b"\033[6n")
            buf = b""
            for _ in range(32):
                if not select.select([fd], [], [], 0.3)[0]:
                    break
                ch = os.read(fd, 1)
                buf += ch
                if ch == b"R":
                    break
            m = re.search(rb"\033\[(\d+);(\d+)R", buf)
            if m:
                return int(m.group(1))
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except Exception:
        pass
    return None

def show_avatar(url: str, auth_headers: dict | None = None, max_cols: int = 35,
                at_row: int | None = None):
    """Render machine avatar via kitten icat. Returns (success, img_rows)."""
    import tempfile
    if not _kitty_available():
        return (False, 0)
    data = _img_bytes(url, headers=auth_headers) or _img_bytes(url)
    if not data:
        return (False, 0)
    suffix = ".jpg" if data[:3] == b"\xff\xd8\xff" else ".png"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(data); tmp.close()
    try:
        img_rows = max(max_cols // 2, 8)

        if at_row is not None:
            place_arg = f"{max_cols}x{img_rows}@0x{at_row}"
            result = subprocess.run(
                ["kitten", "icat", "--align", "left", "--scale-up",
                 "--place", place_arg, tmp.name]
            )
            return (result.returncode == 0, img_rows)

        cursor_row = _query_cursor_y()
        if cursor_row is not None:
            place_arg = f"{max_cols}x{img_rows}@0x{cursor_row - 1}"
            result = subprocess.run(
                ["kitten", "icat", "--align", "left", "--scale-up",
                 "--place", place_arg, tmp.name]
            )
            sys.stdout.write(f"\033[{img_rows}B\n")
            sys.stdout.flush()
        else:
            result = subprocess.run(
                ["kitten", "icat", "--align", "left", tmp.name]
            )
            sys.stdout.write("\n"); sys.stdout.flush()
        return (result.returncode == 0, img_rows)
    finally:
        try: os.unlink(tmp.name)
        except Exception: pass

def os_label(os_name: str) -> str:
    low = (os_name or "").lower()
    if "windows" in low: return "Windows"
    if "linux"   in low: return "Linux"
    if "freebsd" in low: return "FreeBSD"
    if "android" in low: return "Android"
    return os_name or "Unknown"

def diff_color(d: str) -> str:
    return DIFF_COLORS.get(d, "white")

def own_mark(owned: bool) -> str:
    return "[bold green]YES[/]" if owned else "[dim] NO[/]"

def progress_bar(value: int, total: int, width: int = 24) -> str:
    if not total:
        return "[dim]—[/dim]"
    pct    = min(value / total, 1.0)
    filled = int(pct * width)
    bar    = "=" * filled + "-" * (width - filled)
    color  = "red" if pct < 0.4 else "yellow" if pct < 0.7 else "green"
    return f"[{color}][{bar}][/] [dim]{value}/{total}[/dim]"



def _banner_login_status() -> str:
    from dotenv import load_dotenv

    from ctrl_cli.cache import BASE_URL, get_runtime_token
    from ctrl_cli.config import resolve_auth_token

    load_dotenv()
    token = get_runtime_token() or resolve_auth_token()
    if not token:
        return "[bold red]not logged in[/bold red]"

    try:
        import requests

        r = requests.get(
            f"{BASE_URL}/user/info",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "User-Agent": f"HTB-CTRL/{VERSION}",
            },
            timeout=3,
        )
        if r.ok:
            data = r.json()
            if isinstance(data, dict):
                info = data.get("info", data)
                if isinstance(info, dict):
                    name = info.get("name")
                    if name:
                        return f"logged in as [bold green]{name}[/bold green]"
    except Exception:
        pass
    return "[bold red]not logged in[/bold red]"


def print_banner(hide_banner: bool = False):
    if hide_banner:
        return
    console.print()
    if BANNER_FILE.is_file():
        console.print(BANNER_FILE.read_text(), end="")
    console.print()
    status = _banner_login_status()
    console.print(
        f"\nHTB CTRL v{VERSION} by yonasuriv  ·  {status}",
        style="dim",
        justify="left",
        highlight=False,
    )
    console.print()

_S = "[yellow]STRING[/yellow]"
_I = "[cyan]INT[/cyan]"
_HELP_BORDER = "dim"


def _strip_markup(text: str) -> str:
    return re.sub(r"\[/?[^\]]+\]", "", text)


def _help_section(title: str, rows: list[tuple[str, str]], *, cmd_width: int) -> Panel:
    tbl = Table(box=None, show_header=False, padding=(0, 2), expand=True)
    tbl.add_column(style="bold cyan", width=cmd_width, no_wrap=True)
    tbl.add_column(style="dim", ratio=1, no_wrap=False)
    for cmd, desc in rows:
        tbl.add_row(cmd, desc)
    return Panel(
        tbl,
        title=f"[bold white] {title} [/bold white]",
        title_align="center",
        border_style=_HELP_BORDER,
        padding=(0, 1),
    )


def _print_help_sections(sections: list[tuple[str, list[tuple[str, str]]]]) -> None:
    cmd_width = max(
        (len(_strip_markup(cmd)) for _, rows in sections for cmd, _ in rows),
        default=20,
    ) + 2
    for title, rows in sections:
        console.print(_help_section(title, rows, cmd_width=cmd_width))


def _menu_section(title, color, rows):
    tbl = Table(box=None, show_header=False, padding=(0, 2), expand=True)
    tbl.add_column(style="bold cyan", min_width=20, no_wrap=True)
    tbl.add_column(style="dim", ratio=1, no_wrap=False)
    for cmd, desc in rows:
        tbl.add_row(cmd, desc)
    return Panel(tbl, title=f"[bold white] {title} [/bold white]",
                 title_align="center", border_style=color, padding=(0, 1))


def print_menu(hide_banner: bool = False):
    print_banner(hide_banner=hide_banner)
    console.print(_menu_section("MACHINES", "bright_green", [
        ("machines",     "List / search active or retired machines  —  uses local cache"),
        ("machine", "Full details: OS, avatar image, difficulty, solves, tags"),
        ("submit",       "Submit user or root flag"),
    ]))
    console.print(_menu_section("LABS", "yellow", [
        ("active", "Show the machine currently running and its assigned IP"),
        ("spawn",  "Start (spawn) a machine in your lab"),
        ("stop",   "Stop the active machine  (auto-detects ID when omitted)"),
        ("reset",  "Reset a machine back to its initial state"),
    ]))
    console.print(_menu_section("TOOLS", "blue", [
        ("metrics",   "Fetch HTB profile data"),
        ("badge",     "Generate profile badge"),
        ("dashboard", "HTB machines cheat sheet in the browser"),
    ]))
    console.print(_menu_section("SETTINGS", "red", [
        ("auth",    "Configure and verify your HTB API token"),
        ("profile", "Profile stats, ranking, owns, bloods and rank progress"),
        ("cache",   "View or clear local machine cache  (active 1h · retired 24h)"),
    ]))
    console.print(
        "\n  [dim]Run `htbctrl --help` for the full command reference or "
        "`htbctrl COMMAND --help` for per-command options.[/dim]\n"
    )


def print_help(hide_banner: bool = False):
    print_banner(hide_banner=hide_banner)
    console.print(Rule(style="dim green"))
    console.print()
    console.print("[bold]HTB Ctrl — Command Reference[/bold]\n")

    _print_help_sections([
        ("GLOBAL FLAGS", [
        ("--from-env",       "Load token/settings from .env (env wins over CLI/YAML)"),
        (f"--env-file {_S}", "Dotenv path for --from-env  [default: .env]"),
        (f"--config {_S}",   "CLI YAML config  [default: htb-cli.yml]"),
        ("--metrics-config", "Metrics YAML fallback for shared token keys"),
        (f"--api-token {_S}", "HTB app API token"),
        (f"--bearer {_S}",  "HTB bearer token"),
        ("--hide-banner",    "Suppress startup banner on help"),
    ]),
        ("MACHINES", [
        ("machines",              "List active machines (cached)"),
        ("  --retired, -r",       "Include retired machines (VIP)"),
        (f"  --os, -o {_S}",       "Filter by OS (linux, windows, …)"),
        (f"  --diff, -d {_S}",     "Filter by difficulty"),
        (f"  --search, -s {_S}",   "Search by machine name"),
        ("  --owned",             "Show only fully owned"),
        ("  --pending",           "Show only unowned"),
        (f"  --limit, -l {_I}",    "Limit result count"),
        ("  --refresh, -f",       "Force cache refresh"),
        (f"machine --id, -i {_I}", "Detailed machine view (avatar on Kitty)"),
        ("  --debug",             "Dump raw API fields (hidden)"),
        (f"submit --id -i {_I} --flag -f {_S}", "Submit user/root flag"),
        ("  --type, -t user|root",   "Flag type (auto-detected if omitted)"),
        (f"  --diff, -d {_I}",        "Perceived difficulty rating (1–10)"),
    ]),
        ("LABS", [
        ("active",           "Show running machine and IP"),
        (f"spawn --id, -i {_I}", "Start a machine"),
        ("  --vip",            "Use VIP server"),
        (f"stop [--id, -i {_I}]",   "Stop machine (auto-detect if omitted)"),
        (f"reset [--id, -i {_I}]",  "Reset machine to initial state"),
    ]),
        ("METRICS", [
        ("metrics", "Fetch HTB API JSON → user/<id>/data/"),
        ("badge", "Fetch + render badge → user/<id>/"),
        ("  --generate-badge", "Generate profile badge"),
        (f"  -p, --profile {_I}",     "6-digit HTB profile ID"),
        (f"  -t, --template {_S}",  "Template name"),
        (f"  -o, --output-dir {_S}", "Badge output dir"),
        (f"  --config {_S}",         "Metrics YAML  [default: htb-metrics.yml]"),
        ("  --no-cache",            "Disable API response cache"),
        ("  --from-env",            "Load from .env (metrics scope)"),
        (f"  --env-file {_S}",       "Dotenv for --from-env"),
        (f"  --api-token / --token / --bearer {_S}", "HTB auth token"),
    ]),
        ("DASHBOARD", [
        ("dashboard",              "Open offline in browser (file picker)"),
        ("dashboard --serve",      "Serve on http://127.0.0.1:8080"),
        (f"dashboard --port {_I}",  "Port for --serve  [default: 8080]"),
        ("dashboard --new-sheet",  "Create htb_machines.xlsx at repo root"),
        ("  --force",              "Overwrite existing spreadsheet with --new-sheet"),
    ]),
        ("SETTINGS", [
        (f"auth --token, -t {_S}", "Save and verify HTB API token"),
        ("profile", "Profile stats, ranking, owns, bloods"),
        ("cache", "Show cache status"),
        ("cache --clear, -c", "Clear machine cache"),
        ("cache --status, -s", "Show cache age and validity"),
    ]),
        ("ENVIRONMENT", [
        ("HTB_PROFILE_ID",   "6-digit profile ID (metrics/badges)"),
        ("HTB_API_TOKEN",    "App API token"),
        ("HTB_TOKEN",        "Token alias"),
        ("HTB_BEARER",       "Bearer alias"),
        ("HTB_TEMPLATE",     "Badge template name"),
        ("HTB_OUTPUT_DIR",   "Badge output directory"),
        ("HTB_CACHE_DIR",    "API data cache directory"),
        ("HTB_CACHE_TTL",    "Cache TTL in seconds"),
        ("HTB_NO_CACHE",     "Disable cache when true"),
        ("HTB_HIDE_IF_NULL", "Hide empty badge fields"),
        ("HTBCTRL_SKIP_BOOTSTRAP", "Skip venv bootstrap (CI/tests)"),
    ]),
    ])

    console.print(
        "\n  [dim]Run `htbctrl COMMAND --help` for per-command typer help.\n"
        "  User docs: https://github.com/yonasuriv/htb-ctrl/blob/main/docs/guides/README.md[/dim]"
    )

