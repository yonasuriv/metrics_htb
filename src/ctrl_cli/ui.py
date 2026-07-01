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



def print_banner(hide_banner: bool = False):
    if hide_banner:
        return
    console.print()
    if BANNER_FILE.is_file():
        console.print(BANNER_FILE.read_text(), end="")
    console.print()
    console.print(
        f"\nHTB CTRL v{VERSION}  ·  by [bold green]yonasuriv[/bold green]",
        style="dim",
        justify="left",
        highlight=False,
    )
    console.print()

def _help_section(title, color, rows):
    tbl = Table(box=None, show_header=False, padding=(0, 2), expand=True)
    tbl.add_column(style="bold cyan", min_width=20, no_wrap=True)
    tbl.add_column(style="dim", ratio=1, no_wrap=False)
    for cmd, desc in rows:
        tbl.add_row(cmd, desc)
    return Panel(tbl, title=f"[bold white] {title} [/bold white]",
                 title_align="center", border_style=color, padding=(0, 1))

def print_help(hide_banner: bool = False):
    print_banner(hide_banner=hide_banner)
    console.print(Rule(style="dim green"))
    console.print()
    console.print(_help_section("MACHINES", "bright_green", [
        ("machines",     "List / search active or retired machines  —  uses local cache"),
        ("machine-info", "Full details: OS, avatar image, difficulty, solves, tags"),
        ("submit",       "Submit user or root flag"),
    ]))
    console.print(_help_section("LABS", "yellow", [
        ("active", "Show the machine currently running and its assigned IP"),
        ("spawn",  "Start (spawn) a machine in your lab"),
        ("stop",   "Stop the active machine  (auto-detects ID when omitted)"),
        ("reset",  "Reset a machine back to its initial state"),
    ]))
    console.print(_help_section("TOOLS", "blue", [
        ("metrics",   "Fetch HTB profile data"),
        ("badges",    "Generate profile badge PNG/SVG"),
        ("dashboard", "HTB machines cheat sheet in the browser"),
    ]))
    console.print(_help_section("SETTINGS", "magenta", [
        ("auth",    "Configure and verify your HTB API token"),
        ("profile", "Profile stats, ranking, owns, bloods and rank progress"),
        ("cache",   "View or clear local machine cache  (active 1h · retired 24h)"),
    ]))
    console.print(
        "\n  [dim]Run `htbctrl COMMAND --help` for per-command detailed options or `htbctrl man` for full reference manual.[/dim]\n"
    )

