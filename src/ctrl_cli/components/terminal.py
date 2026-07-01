from __future__ import annotations

import io
import json
import sys
import time

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ctrl_cli.api import api_get, api_post, fetch_machines
from ctrl_cli.cache import (
    ACTIVE_IMG_COLS,
    CACHE_FILE,
    CACHE_TTL,
    CONFIG_FILE,
    MACHINE_INFO_IMG_COLS,
    cache_clear,
    get_headers,
    load_config,
    save_config,
)
from ctrl_cli.ui import (
    _kitty_available,
    _query_cursor_y,
    console,
    diff_color,
    os_label,
    own_mark,
    progress_bar,
    show_avatar,
)


def register(app: typer.Typer) -> None:

    @app.command("auth")
    def auth(
        token: str = typer.Option(..., "--token", "-t",
                                  help="App Token (HTB → Settings → API Key)"),
    ):
        """Configure and verify your HTB API token."""
        if not token.startswith("eyJ") or len(token) < 50:
            console.print("[yellow]Warning:[/] Token doesn't look like a standard JWT (should start with eyJ...)." + "\n")
            if not typer.confirm("Continue anyway?"):
                raise typer.Exit(0)

        save_config({"token": token})

        me = api_get("/user/info", silent=True)
        if me and isinstance(me, dict):
            info = me.get("info", me)
            name = info.get("name", "?")
            console.print(Panel(
                f"[bold green]Token valid[/bold green]\n\n"
                f"  Logged in as:  [bold cyan]{name}[/bold cyan]\n"

                f"  Config file:   [dim]{CONFIG_FILE}[/dim]",
                title="HTB Auth", border_style="green",
            ))
        else:
            console.print(Panel(
                "[yellow]Token saved but API did not respond.[/yellow]\n"
                "[dim]May be temporary or the token is incorrect.[/dim]",
                border_style="yellow",
            ))

    @app.command("machines")
    def machines(
        retired:     bool = typer.Option(False, "--retired",  "-r",
                                         help="Show retired machines (requires VIP)"),
        os_filter:   str  = typer.Option("",    "--os",       "-o",
                                         help="Filter by OS: linux / windows / freebsd"),
        diff_filter: str  = typer.Option("",    "--diff",     "-d",
                                         help="Filter by difficulty: Easy / Medium / Hard / Insane"),
        search:      str  = typer.Option("",    "--search",   "-s",
                                         help="Search by name (uses cache, searches both active + retired)"),
        owned:       bool = typer.Option(False, "--owned",
                                         help="Only fully completed machines (user + root)"),
        pending:     bool = typer.Option(False, "--pending",
                                         help="Only machines not yet completed"),
        limit:       int  = typer.Option(0,     "--limit",    "-l",
                                         help="Max results to show (0 = no limit)"),
        force:       bool = typer.Option(False, "--refresh",  "-f",
                                         help="Ignore cache and fetch fresh data"),
    ):
        """List and search HTB machines with filters and local cache."""

        if search:
            active_list  = fetch_machines(retired=False, force=force)
            retired_list = fetch_machines(retired=True,  force=force)
            machines_list = active_list + retired_list
        else:
            machines_list = fetch_machines(retired=retired, force=force)

        if not machines_list:
            console.print(
                "[red]Error:[/] No machines returned from API.\n"
                "  Check your token: [cyan]htbctrl auth --token YOUR_TOKEN[/]"
            )
            raise typer.Exit(1)

        total_raw = len(machines_list)

        if search:
            q = search.lower()
            machines_list = [m for m in machines_list
                             if q in (m.get("name") or "").lower()]

        if os_filter:
            machines_list = [m for m in machines_list
                             if os_filter.lower() in (m.get("os") or "").lower()]

        if diff_filter:
            machines_list = [m for m in machines_list
                             if diff_filter.lower() == (m.get("difficultyText") or "").lower()]

        if owned:
            machines_list = [m for m in machines_list
                             if m.get("authUserInUserOwns") and m.get("authUserInRootOwns")]

        if pending:
            machines_list = [m for m in machines_list
                             if not (m.get("authUserInUserOwns") and m.get("authUserInRootOwns"))]

        seen, unique = set(), []
        for m in machines_list:
            mid = m.get("id")
            if mid not in seen:
                seen.add(mid)
                unique.append(m)
        machines_list = unique

        machines_list.sort(key=lambda m: m.get("id", 0))

        if limit > 0:
            machines_list = machines_list[:limit]

        if not machines_list:
            console.print("\n[yellow]No results with the applied filters.[/]\n")
            raise typer.Exit(0)

        if search:
            title_mode = f"Search: '{search}'"
        elif retired:
            title_mode = "Retired"
        else:
            title_mode = "Active"

        count_note = f"{len(machines_list)}"
        if len(machines_list) != total_raw:
            count_note += f" of {total_raw}"

        table = Table(
            title=f"HTB Machines — {title_mode}  [{count_note}]",
            box=box.ROUNDED,
            border_style="bright_green",
            header_style="bold cyan",
            show_lines=True,
        )

        table.add_column("ID",         style="dim",        width=6,  justify="right")
        table.add_column("Name",       style="bold white",  width=18)
        table.add_column("OS",                              width=14)
        table.add_column("Difficulty",                      width=12, justify="center")
        table.add_column("Pts",                             width=5,  justify="center")
        table.add_column("Rating",                          width=7,  justify="center")
        table.add_column("User",                            width=6,  justify="center")
        table.add_column("Root",                            width=6,  justify="center")
        table.add_column("Release",    style="dim",         width=12)
        if search:
            table.add_column("Status",                      width=10, justify="center")

        for m in machines_list:
            d       = m.get("difficultyText", "?")
            os_name = m.get("os", "?")
            star    = m.get("star") or 0

            row = [
                str(m.get("id", "?")),
                m.get("name", "?"),
                os_label(os_name),
                f"[{diff_color(d)}]{d}[/]",
                str(m.get("points") or "—"),
                f"[yellow]{star:.1f}[/]" if star else "[dim]—[/]",
                own_mark(m.get("authUserInUserOwns")),
                own_mark(m.get("authUserInRootOwns")),
                (m.get("release") or "")[:10],
            ]
            if search:
                is_ret = m.get("retired", False)
                row.append("[red]Retired[/]" if is_ret else "[green]Active[/]")

            table.add_row(*row)

        console.print()
        console.print(table)
        console.print(
            "\n[dim]"
            "Info:  htbctrl machine --id ID  |  "
            "Flag:  htbctrl submit --id ID --flag FLAG  |  "
            "Start: htbctrl spawn --id ID"
            "[/dim]\n"
        )

    @app.command("machine")
    def machine(
        machine_id: int  = typer.Option(..., "--id", "-i", help="Machine ID"),
        debug:      bool = typer.Option(False, "--debug",     hidden=True, help="Dump raw API fields"),
    ):
        """Show detailed information for a single machine."""
        data = api_get(f"/machine/profile/{machine_id}")
        if not data:
            console.print(f"[red]Error:[/] Machine {machine_id} not found.")
            raise typer.Exit(1)

        m        = data.get("info", data) if isinstance(data, dict) else {}

        if debug:
            console.print("\n[bold yellow]--- RAW API FIELDS ---[/bold yellow]")
            for k, v in sorted(m.items()):
                if k not in ("tags", "hints", "solves"):
                    console.print(f"  [cyan]{k:<30}[/cyan] {repr(v)[:80]}")
            console.print("[bold yellow]--- END ---[/bold yellow]\n")
            raise typer.Exit(0)

        d        = m.get("difficultyText", "?")
        os_name  = m.get("os", "?")
        star     = m.get("stars", 0) or 0
        name     = m.get("name", "?")
        retired  = m.get("retired", False)
        pts      = m.get("points", "?")
        release  = (m.get("release") or "")[:10]
        u_count  = m.get("user_owns_count", m.get("userOwnCount", "?"))
        r_count  = m.get("root_owns_count", m.get("systemOwnCount", "?"))
        tags_list  = [tg.get("name","") for tg in (m.get("tags") or []) if tg.get("name")]
        hints_list = m.get("hints") or []

        W = 16
        diff_str = f"[{diff_color(d)}]{d}[/]"
        stat_str = "[red]Retired[/]" if retired else "[green]Active[/]"
        u_str = ("  [bold green]Owned[/]" if m.get("authUserInUserOwns") else "  [dim]Pending[/]") + f"  [dim]({u_count} solves)[/dim]"
        r_str = ("  [bold green]Owned[/]" if m.get("authUserInRootOwns") else "  [dim]Pending[/]") + f"  [dim]({r_count} solves)[/dim]"

        def irow(lbl, val):
            return f"  [bold cyan]{lbl:<{W}}[/bold cyan]{val}" + chr(10)

        info = chr(10)
        info += irow("OS",         os_label(os_name))
        info += irow("Difficulty", diff_str)
        info += irow("Points",     str(pts))
        info += irow("Rating",     f"[yellow]{star:.1f} / 5[/yellow]")
        info += irow("Release",    f"[dim]{release}[/dim]")
        info += irow("Status",     stat_str)
        info += chr(10)
        info += irow("User Flag",  u_str)
        info += irow("Root Flag",  r_str)

        if tags_list:
            info += chr(10) + irow("Tags", "[dim]" + ", ".join(tags_list) + "[/dim]")
        if hints_list:
            info += irow("Hints", f"[dim]{len(hints_list)} available[/dim]")

        info_panel = Panel(
            info,
            title=f"[bold green]{name}[/bold green]  [dim]#{machine_id}[/dim]",
            title_align="center",
            border_style="bright_green",
            padding=(1, 2),
        )

        _av = m.get("avatar") or ""
        if _av and _av.startswith("/"):
            _av = "https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com" + _av

        IMG_COLS = MACHINE_INFO_IMG_COLS
        avatar_shown = False

        if _av and _kitty_available():
            import shutil
            term_w = shutil.get_terminal_size((120, 24)).columns
            panel_w = max(term_w - IMG_COLS - 4, 45)
            img_rows = max(IMG_COLS // 2, 8)

            buf = io.StringIO()
            rc  = Console(file=buf, width=panel_w, force_terminal=True,
                          color_system="truecolor")
            rc.print(info_panel)
            panel_lines = buf.getvalue().rstrip("\n").split("\n")

            console.print()
            start_row = _query_cursor_y()

            if start_row is not None:
                total_lines = max(len(panel_lines), img_rows + 2)
                sys.stdout.write("\n" * total_lines)
                sys.stdout.flush()

                end_row = _query_cursor_y()
                if end_row is not None:
                    area_top_1 = end_row - total_lines
                    area_top_0 = max(area_top_1 - 1, 0)

                    avatar_shown, _ = show_avatar(
                        _av, auth_headers=get_headers(),
                        max_cols=IMG_COLS, at_row=area_top_0,
                    )

                    text_col = IMG_COLS + 3
                    for i, line in enumerate(panel_lines):
                        r = area_top_1 + i
                        if r >= 1:
                            sys.stdout.write(f"\033[{r};{text_col}H{line}")

                    sys.stdout.write(f"\033[{end_row};1H")
                    sys.stdout.flush()

        if not avatar_shown:
            if _av and _kitty_available():
                show_avatar(_av, auth_headers=get_headers(), max_cols=IMG_COLS)
            console.print()
            console.print(info_panel)

        console.print(
            f"[dim]  Submit : htbctrl submit --id {machine_id} --flag FLAG --type user|root[/dim]" + chr(10) +
            f"[dim]  Spawn  : htbctrl spawn --id {machine_id}[/dim]" + chr(10)
        )


    @app.command("submit")
    def submit(
        machine_id: int = typer.Option(..., "--id",   "-i", help="Machine ID"),
        flag:       str = typer.Option(..., "--flag", "-f", help="Captured flag (32 hex chars)"),
        flag_type:  str = typer.Option("", "--type", "-t", help="Flag type: user or root (auto-detected if omitted)"),
        difficulty: int = typer.Option(0,  "--diff", "-d", help="Perceived difficulty 1-10 (0 = skip)"),
    ):
        """Submit a user or root flag to Hack The Box."""
        flag = flag.strip()
        flag_type = flag_type.strip().lower()

        # Auto-detect flag type: if user is already owned → root
        if not flag_type:
            profile_data = api_get(f"/machine/profile/{machine_id}", silent=True)
            pm = {}
            if profile_data and isinstance(profile_data, dict):
                pm = profile_data.get("info", profile_data)

            user_owned = pm.get("authUserInUserOwns", False)
            root_owned = pm.get("authUserInRootOwns", False)

            if user_owned and root_owned:
                console.print(Panel(
                    f"[bold yellow]Machine #{machine_id} is already fully owned![/bold yellow]\n\n"
                    "  [dim]Both user and root flags have been submitted.[/dim]",
                    title="[bold yellow]Already Owned[/bold yellow]",
                    border_style="yellow",
                ))
                return

            flag_type = "root" if user_owned else "user"
        else:
            profile_data = api_get(f"/machine/profile/{machine_id}", silent=True)
            pm = {}
            if profile_data and isinstance(profile_data, dict):
                pm = profile_data.get("info", profile_data)
            if flag_type == "user" and pm.get("authUserInUserOwns"):
                console.print(Panel(
                    f"[bold yellow]User flag already submitted for #{machine_id}[/bold yellow]",
                    border_style="yellow",
                ))
                return
            if flag_type == "root" and pm.get("authUserInRootOwns"):
                console.print(Panel(
                    f"[bold yellow]Root flag already submitted for #{machine_id}[/bold yellow]",
                    border_style="yellow",
                ))
                return

        if flag_type not in ("user", "root"):
            console.print("[red]Error:[/] Invalid type — use [cyan]user[/] or [cyan]root[/]")
            raise typer.Exit(1)

        if difficulty and not (1 <= difficulty <= 10):
            console.print("[red]Error:[/] Difficulty must be between 1 and 10.")
            raise typer.Exit(1)

        payload = {"id": machine_id, "flag": flag}
        if difficulty:
            payload["difficulty"] = difficulty * 10

        result = api_post("/machine/own", payload, silent=True)

        if result is None:
            console.print(Panel(
                "[bold red]No response from API.[/bold red]\n\n"
                "  [dim]Check your connection and try again.[/dim]",
                title="[bold red]Error[/bold red]",
                border_style="red",
            ))
            raise typer.Exit(1)

        message = result.get("message", "")

        already_phrases = ["already", "been owned", "previously"]
        is_already = any(p in message.lower() for p in already_phrases)

        fail_phrases = ["incorrect", "wrong", "invalid flag", "can not be accessed", "not found"]
        is_fail = any(p in message.lower() for p in fail_phrases)

        success = (
            not is_fail
            and (
                result.get("success") is True
                or "Owned"   in message
                or "correct" in message.lower()
                or "congrat" in message.lower()
            )
        )

        label = "USER" if flag_type == "user" else "ROOT"

        if is_already:
            console.print(Panel(
                f"[bold yellow]{label} flag already submitted[/bold yellow]\n\n"
                f"  Machine:  [cyan]{machine_id}[/cyan]\n"
                + (f"\n  [dim]{message}[/dim]" if message else ""),
                title="[bold yellow]Already Owned[/bold yellow]",
                border_style="yellow",
            ))
        elif success:
            diff_str = f"\n  Difficulty: [white]{difficulty}/10[/white]" if difficulty else ""
            console.print(Panel(
                f"[bold green]{label} flag correct — PWN3D![/bold green]\n\n"
                f"  Machine:    [cyan]{machine_id}[/cyan]\n"
                f"  Type:       [white]{label}[/white]"
                + diff_str + "\n"
                + (f"\n  [dim]{message}[/dim]" if message else ""),
                title="[bold green]Owned![/bold green]",
                border_style="green",
            ))
        else:
            console.print(Panel(
                f"[bold red]Incorrect flag[/bold red]\n\n"
                f"  [dim]{message or str(result)}[/dim]",
                title="[bold red]Failed[/bold red]",
                border_style="red",
            ))

    @app.command("active")
    def active_machine():
        """Show the machine you currently have running."""
        data = api_get("/machine/active", silent=True)

        if not data or not isinstance(data, dict):
            console.print(Panel(
                "[dim]No active machine at the moment.\n\n"
                "  Start one with:  [white]htbctrl spawn --id ID[/white][/dim]",
                border_style="yellow",
            ))
            return

        m = data.get("info", data)
        if not m or not m.get("id"):
            console.print(Panel(
                "[dim]No active machine.\n\n"
                "  Start one with:  [white]htbctrl spawn --id ID[/white][/dim]",
                border_style="yellow",
            ))
            return

        mid     = m.get("id", "?")
        name    = m.get("name", "?")
        ip      = m.get("ip", m.get("server", "—"))
        expires = m.get("expires_at", "")

        d, os_name, _av = "?", "?", ""
        pm = {}
        profile = api_get(f"/machine/profile/{mid}", silent=True)
        if profile:
            pm      = profile.get("info", profile) if isinstance(profile, dict) else {}
            d       = pm.get("difficultyText", m.get("difficultyText", "?"))
            os_name = pm.get("os",             m.get("os", "?"))
            _av     = pm.get("avatar") or m.get("avatar") or ""

        if _av and _av.startswith("/"):
            _av = "https://htb-mp-prod-public-storage.s3.eu-central-1.amazonaws.com" + _av

        W = 16
        def irow(lbl, val):
            return f"  [bold cyan]{lbl:<{W}}[/bold cyan]{val}" + chr(10)

        info = chr(10)
        info += irow("IP",         f"[bold cyan]{ip}[/bold cyan]")
        info += irow("OS",         os_label(os_name))
        info += irow("Difficulty", f"[{diff_color(d)}]{d}[/]")
        if expires:
            info += irow("Expires", f"[dim]{expires}[/dim]")

        u_me = "[green]Owned[/]" if pm.get("authUserInUserOwns") else "[dim]Pending[/]"
        r_me = "[green]Owned[/]" if pm.get("authUserInRootOwns") else "[dim]Pending[/]"
        info += chr(10)
        info += irow("User Flag", u_me)
        info += irow("Root Flag", r_me)

        info_panel = Panel(
            info,
            title=f"[bold green]{name}[/bold green]  [dim]#{mid}[/dim]",
            title_align="center",
            border_style="green",
            padding=(1, 2),
        )

        IMG_COLS = ACTIVE_IMG_COLS
        avatar_shown = False

        if _av and _kitty_available():
            import shutil
            term_w = shutil.get_terminal_size((120, 24)).columns
            panel_w = max(term_w - IMG_COLS - 4, 45)
            img_rows = max(IMG_COLS // 2, 8)

            buf = io.StringIO()
            rc  = Console(file=buf, width=panel_w, force_terminal=True,
                          color_system="truecolor")
            rc.print(info_panel)
            panel_lines = buf.getvalue().rstrip("\n").split("\n")

            console.print()
            start_row = _query_cursor_y()

            if start_row is not None:
                total_lines = max(len(panel_lines), img_rows + 2)
                sys.stdout.write("\n" * total_lines)
                sys.stdout.flush()

                end_row = _query_cursor_y()
                if end_row is not None:
                    area_top_1 = end_row - total_lines
                    area_top_0 = max(area_top_1 - 1, 0)

                    avatar_shown, _ = show_avatar(
                        _av, auth_headers=get_headers(),
                        max_cols=IMG_COLS, at_row=area_top_0,
                    )

                    text_col = IMG_COLS + 3
                    for i, line in enumerate(panel_lines):
                        r = area_top_1 + i
                        if r >= 1:
                            sys.stdout.write(f"\033[{r};{text_col}H{line}")

                    sys.stdout.write(f"\033[{end_row};1H")
                    sys.stdout.flush()

        if not avatar_shown:
            if _av and _kitty_available():
                show_avatar(_av, auth_headers=get_headers(), max_cols=IMG_COLS)
            console.print()
            console.print(info_panel)

        console.print(
            f"[dim]  Stop:   htbctrl stop  |  "
            f"Reset:  htbctrl reset  |  "
            f"Flag:   htbctrl submit --id {mid} --flag FLAG[/dim]\n"
        )

    @app.command("spawn")
    def spawn(
        machine_id: int  = typer.Option(..., "--id",  "-i",  help="Machine ID to start"),
        vip:        bool = typer.Option(False, "--vip",       help="Use VIP server"),
    ):
        """Start (spawn) a machine on HTB."""

        payload = {"machine_id": machine_id}
        if vip:
            payload["is_vip"] = True

        result = api_post("/vm/spawn",       payload,             silent=True)
        if not result:
            result = api_post("/machine/play",  {"id": machine_id}, silent=True)
        if not result:
            result = api_post("/machine/start", {"id": machine_id}, silent=False)

        if not result:
            raise typer.Exit(1)

        message = result.get("message", "")
        success = result.get("success", True)

        failure_phrases = [
            "cannot spawn", "non-free", "free server", "vip", "subscribe",
            "already running", "no slot", "upgrade",
        ]
        is_error = (
            not success
            or any(p in message.lower() for p in failure_phrases)
        )

        if is_error:
            console.print(Panel(
                f"[bold red]Spawn failed[/bold red]\n\n"
                f"  [yellow]{message}[/yellow]\n\n"
                f"  [dim]This machine requires a VIP / VIP+ subscription.[/dim]\n"
                f"  [dim]Upgrade at: https://app.hackthebox.com/billing[/dim]",
                title="[bold red]Spawn Error[/bold red]",
                border_style="red",
            ))
        else:
            console.print(Panel(
                f"[bold green]Machine #{machine_id} is starting up[/bold green]\n\n"
                f"  [dim]{message or 'Machine queued — usually ready in ~30s'}[/dim]\n\n"
                f"  [dim]Check IP:  htbctrl active[/dim]",
                title="[bold green]Spawn OK[/bold green]",
                border_style="green",
            ))

    @app.command("stop")
    def stop(
        machine_id: int = typer.Option(0, "--id", "-i",
                                        help="Machine ID (0 = auto-detect active)"),
    ):
        """Stop the active HTB machine."""
        if not machine_id:
            data = api_get("/machine/active", silent=True)
            if data and isinstance(data, dict):
                m = data.get("info") or data
                if isinstance(m, dict):
                    machine_id = m.get("id", 0)

        if not machine_id:
            console.print(Panel(
                "[dim]No active machine found.\n\n"
                "  Start one with:  [white]htbctrl spawn --id ID[/white][/dim]",
                border_style="yellow",
            ))
            raise typer.Exit(0)


        result = api_post("/vm/terminate",   {"machine_id": machine_id}, silent=True)
        if not result:
            result = api_post("/machine/stop",   {"id": machine_id}, silent=True)
        if not result:
            result = api_post("/machine/expiry", {"id": machine_id}, silent=False)

        if not result:
            raise typer.Exit(1)

        message = result.get("message", "")
        console.print(Panel(
            f"[bold green]Machine #{machine_id} stopped[/bold green]\n"
            + (f"\n  [dim]{message}[/dim]" if message else ""),
            title="[bold green]Stopped[/bold green]",
            border_style="green",
        ))

    @app.command("reset")
    def reset(
        machine_id: int = typer.Option(0, "--id", "-i",
                                        help="Machine ID (0 = auto-detect active)"),
    ):
        """Reset the active HTB machine to its initial state."""
        if not machine_id:
            data = api_get("/machine/active", silent=True)
            if data and isinstance(data, dict):
                m = data.get("info") or data
                if isinstance(m, dict):
                    machine_id = m.get("id", 0)

        if not machine_id:
            console.print(Panel(
                "[dim]No active machine to reset.\n\n"
                "  Start one with:  [white]htbctrl spawn --id ID[/white][/dim]",
                border_style="yellow",
            ))
            raise typer.Exit(0)

        result = api_post("/vm/reset", {"machine_id": machine_id}, silent=True)
        if not result:
            result = api_post("/machine/reset", {"id": machine_id}, silent=True)
        if not result:
            result = api_post(f"/machine/reset/{machine_id}", {}, silent=True)

        if not result:
            console.print(Panel(
                f"[bold red]Could not reset machine #{machine_id}[/bold red]\n\n"
                "  [dim]The machine may not support reset or is not active.[/dim]",
                title="[bold red]Reset Error[/bold red]",
                border_style="red",
            ))
            raise typer.Exit(1)

        message = result.get("message", "")
        console.print(Panel(
            f"[bold green]Machine #{machine_id} reset[/bold green]\n"
            + (f"\n  [dim]{message}[/dim]" if message else ""),
            border_style="green",
        ))

    @app.command("profile")
    def profile():
        """Show your profile stats, ranking, owns and activity."""
        me = api_get("/user/info")
        if not me:
            console.print("[red]Error:[/] Could not fetch user info.")
            raise typer.Exit(1)
        info    = me.get("info", me) if isinstance(me, dict) else {}
        user_id = info.get("id")
        full    = api_get(f"/user/profile/basic/{user_id}", silent=True) if user_id else None
        u       = (full.get("profile", full) if isinstance(full, dict) else None) or info

        if not u:
            console.print("[red]Error:[/] Could not fetch profile data.")
            raise typer.Exit(1)

        def g(key, *fallbacks, default: str | int = "—"):
            for k in [key, *fallbacks]:
                v = u.get(k)
                if v not in (None, "", 0, []): return v
            return default

        name         = g("name", default="?")
        rank_label   = g("rank", "rankText",       default="?")
        rank_num     = g("ranking", "rank_id",     default="")
        points       = g("points",                 default=0)
        user_owns    = g("user_owns",   "userOwns",   default=0)
        root_owns    = g("system_owns", "systemOwns", default=0)
        bloods_u     = g("user_bloods",   "userBloods",   default=0)
        bloods_r     = g("system_bloods", "systemBloods", default=0)
        respect      = g("respects",               default=0)
        country      = g("country_name", "country", default="")
        team         = u.get("team") or {}
        team_name    = (team.get("name", "") if isinstance(team, dict) else "") or "—"
        university   = g("university_name", "university", default="")
        joined       = (g("created_at", "createdAt", default="") or "")[:10]
        description  = g("description", default="")
        rp           = u.get("current_rank_progress") or {}
        rank_req     = rp.get("required", 0) if isinstance(rp, dict) else 0
        rank_pts_val = rp.get("current",  0) if isinstance(rp, dict) else 0

        console.print()

        header = f"  [bold white]{name}[/bold white]"
        if country:     header += f"  [dim]{country}[/dim]"
        if description: header += f"\n  [dim italic]{description[:80]}[/dim italic]"
        console.print(Panel(header, border_style="bright_green", padding=(0, 2)))

        rank_str     = f"[bold cyan]{rank_label}[/]" + (f" [dim](#{rank_num} global)[/dim]" if rank_num else "")
        total_owns   = int(user_owns or 0) + int(root_owns or 0)
        total_bloods = int(bloods_u or 0) + int(bloods_r or 0)

        st = Table(box=box.SIMPLE, show_header=False, padding=(0, 3), expand=True)
        st.add_column("K",  style="bold cyan", min_width=22)
        st.add_column("V",  style="white",     min_width=16)
        st.add_column("K2", style="bold cyan", min_width=22)
        st.add_column("V2", style="white",     min_width=16)

        left = [
            ("Rank",          rank_str),
            ("Points",        f"[bold yellow]{points}[/]"),
            ("User Owns",     f"[bold green]{user_owns}[/]"),
            ("Root Owns",     f"[bold green]{root_owns}[/]"),
            ("Total Owns",    f"[bold white]{total_owns}[/]"),
        ]
        right = [
            ("User Bloods",   f"[bold red]{bloods_u}[/]"),
            ("Root Bloods",   f"[bold red]{bloods_r}[/]"),
            ("Total Bloods",  f"[bold red]{total_bloods}[/]"),
            ("Respects",      f"{respect}"),
            ("Team",          team_name),
        ]

        for i in range(max(len(left), len(right))):
            lk, lv = left[i]  if i < len(left)  else ("", "")
            rk, rv = right[i] if i < len(right) else ("", "")
            st.add_row(lk, lv, rk, rv)

        console.print(Panel(st, title="[bold]Stats[/bold]", border_style="cyan", padding=(1, 1)))

        ex = Table(box=box.SIMPLE, show_header=False, padding=(0, 3), expand=True)
        ex.add_column("K",  style="bold cyan", min_width=22)
        ex.add_column("V",  style="white")
        ex.add_column("K2", style="bold cyan", min_width=22)
        ex.add_column("V2", style="white")
        ex.add_row("University", university or "—", "Member since", joined or "—")
        console.print(Panel(ex, border_style="dim", padding=(0, 1)))

        if rank_req and rank_pts_val:
            bar = progress_bar(int(rank_pts_val), int(rank_req), width=26)
            console.print(Panel(
                f"\n  Next rank progress:  {bar}\n",
                title="[bold]Rank Progress[/bold]", border_style="dim",
            ))

    @app.command("cache")
    def cache_cmd(
        clear:  bool = typer.Option(False, "--clear",  "-c", help="Delete all cached data"),
        status: bool = typer.Option(False, "--status", "-s", help="Show cache age and validity"),
    ):
        """Manage the local machine cache."""
        if clear:
            cache_clear()
            console.print("[bold green]Cache cleared.[/]")
            return

        if not CACHE_FILE.exists():
            console.print("[dim]No cache yet.[/dim]")
            return

        try:
            with open(CACHE_FILE) as f:
                data = json.load(f)
        except Exception:
            console.print("[yellow]Warning:[/] Cache file is corrupted.")
            return

        now = time.time()
        t   = Table(box=box.ROUNDED, border_style="cyan", header_style="bold cyan")
        t.add_column("Key",     width=10)
        t.add_column("Entries", width=10, justify="right")
        t.add_column("Age",     width=12)
        t.add_column("TTL",     width=12)
        t.add_column("Status",  width=12, justify="center")

        for key, entry in data.items():
            count   = len(entry.get("data", []))
            age_s   = int(now - entry.get("ts", now))
            ttl     = CACHE_TTL.get(key, 3600)
            valid   = age_s < ttl
            age_m   = age_s // 60
            age_str = f"{age_m}m" if age_m < 60 else f"{age_m // 60}h {age_m % 60}m"
            status_str = "[green]Valid[/]" if valid else "[red]Expired[/]"
            t.add_row(key, str(count), age_str, f"{ttl // 60}m", status_str)

        console.print()
        console.print(t)
        console.print(
            "\n[dim]Clear cache: htbctrl cache --clear  |  "
            "Force refresh: htbctrl machines --refresh[/dim]\n"
        )

