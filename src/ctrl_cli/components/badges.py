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

badges_app = typer.Typer(
    help="Generate HTB profile badges",
    epilog="Run ``htbctrl badges generate --help`` for all flags. Alias: ``htbctrl badge``.",
)


@badges_app.callback(invoke_without_command=True)
def badges_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        typer.echo(OPTION_HELP_EPILOG)
        raise typer.Exit(0)


def _run_generate(
    profile: int | None,
    template: str | None,
    output_dir: str | None,
    config: str,
    no_cache: bool,
    from_env: bool,
    env_file: str,
    api_token: str | None,
    token: str | None,
    bearer: str | None,
) -> None:
    from ctrl_metrics.cli import main as generate_main

    generate_main(
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


@badges_app.command("generate")
def badges_generate(
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
    """Full workflow: fetch data, build dataset, render badge PNG/SVG."""
    _run_generate(
        profile,
        template,
        output_dir,
        config,
        no_cache,
        from_env,
        env_file,
        api_token,
        token,
        bearer,
    )


@badges_app.command("generate-badge", hidden=True)
def badges_generate_legacy(
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
    """Alias for ``badges generate``."""
    _run_generate(
        profile,
        template,
        output_dir,
        config,
        no_cache,
        from_env,
        env_file,
        api_token,
        token,
        bearer,
    )


def register(app: typer.Typer) -> None:
    app.add_typer(badges_app, name="badges")
