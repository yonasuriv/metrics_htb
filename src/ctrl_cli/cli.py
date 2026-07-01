#!/usr/bin/env python3
from __future__ import annotations

from typing import Optional

import typer

from ctrl_cli.cache import set_runtime_token
from ctrl_cli.components import badges, dashboard, metrics, terminal
from ctrl_cli.config import bootstrap_cli_config
from ctrl_cli.ui import print_help

app = typer.Typer(
    help="htbctrl — Hack The Box from your terminal",
    add_completion=False,
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def app_callback(
    ctx: typer.Context,
    from_env: bool = typer.Option(
        False,
        "--from-env",
        help="Load token from .env (env wins over CLI flags and YAML)",
    ),
    env_file: str = typer.Option(".env", "--env-file", help="Dotenv path for --from-env"),
    config: str = typer.Option("htb-cli.yml", "--config", help="CLI YAML config path"),
    metrics_config: str = typer.Option(
        "htb-metrics.yml",
        "--metrics-config",
        help="Fallback metrics YAML config for shared token keys",
    ),
    api_token: Optional[str] = typer.Option(None, "--api-token", help="HTB app API token"),
    bearer: Optional[str] = typer.Option(None, "--bearer", help="HTB bearer token"),
    hide_banner: bool = typer.Option(False, "--hide-banner", help="Suppress startup banner"),
):
    """Global options for env/YAML token resolution."""
    from ctrl_cli.ui import console

    try:
        token = bootstrap_cli_config(
            from_env=from_env,
            env_file=env_file,
            cli_config=config,
            metrics_config=metrics_config,
            cli_api_token=api_token,
            cli_bearer=bearer,
        )
    except ValueError as exc:
        console.print(f"[bold red]{exc}[/]")
        raise typer.Exit(1)
    set_runtime_token(token)
    ctx.obj = {"token": token, "hide_banner": hide_banner}
    if ctx.invoked_subcommand is None:
        print_help(hide_banner=hide_banner)
        raise typer.Exit(0)


@app.command("man", help="Full command and flag reference")
def man_command(ctx: typer.Context):
    """Show all commands, flags, legacy syntax, and environment variables."""
    from ctrl_cli.man import print_man

    obj = ctx.obj or {}
    print_man(hide_banner=obj.get("hide_banner", False))


terminal.register(app)
metrics.register(app)
badges.register(app)
dashboard.register(app)


if __name__ == "__main__":
    from ctrl_cli.ui import console

    console.print()
    app()
