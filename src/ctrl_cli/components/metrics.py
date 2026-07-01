from __future__ import annotations

import typer

from ctrl_cli.components.metrics_opts import (
    ApiTokenOption,
    BearerOption,
    EnvFileOption,
    FromEnvOption,
    MetricsConfigOption,
    NoCacheOption,
    OPTION_HELP_EPILOG,
    OutputDirOption,
    ProfileOption,
    TemplateOption,
    TokenOption,
    build_argv,
)

metrics_app = typer.Typer(
    help="Fetch HTB profile data",
    epilog="Run ``htbctrl metrics pull --help`` or ``htbctrl badges generate --help`` for all flags.",
)


@metrics_app.callback(invoke_without_command=True)
def metrics_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        typer.echo(OPTION_HELP_EPILOG)
        raise typer.Exit(0)


@metrics_app.command("pull")
def metrics_pull(
    profile: ProfileOption = None,
    template: TemplateOption = None,
    output_dir: OutputDirOption = None,
    config: MetricsConfigOption = "htb-metrics.yml",
    no_cache: NoCacheOption = False,
    from_env: FromEnvOption = False,
    env_file: EnvFileOption = ".env",
    api_token: ApiTokenOption = None,
    token: TokenOption = None,
    bearer: BearerOption = None,
):
    """Fetch API data to user/<id>/data JSON files only."""
    from ctrl_metrics.cli import pull_main

    pull_main(
        build_argv(
            profile=profile,
            template=template,
            output_dir=output_dir,
            config=config,
            no_cache=no_cache,
            from_env=from_env,
            env_file=env_file,
            api_token=api_token,
            token=token,
            bearer=bearer,
        )
    )


def register(app: typer.Typer) -> None:
    app.add_typer(metrics_app, name="metrics")
