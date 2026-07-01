from __future__ import annotations

from typing import Annotated, Optional

import typer

ProfileOption = Annotated[
    Optional[int],
    typer.Option("-p", "--profile", help="6-digit HTB profile ID"),
]
TemplateOption = Annotated[
    Optional[str],
    typer.Option("-t", "--template", help="Badge template name"),
]
OutputDirOption = Annotated[
    Optional[str],
    typer.Option("-o", "--output-dir", help="Badge output directory"),
]
MetricsConfigOption = Annotated[
    str,
    typer.Option("--config", help="Metrics YAML config path"),
]
NoCacheOption = Annotated[
    bool,
    typer.Option("--no-cache", help="Disable API response cache"),
]
FromEnvOption = Annotated[
    bool,
    typer.Option(
        "--from-env",
        help="Load settings from .env (env wins over CLI flags and YAML)",
    ),
]
EnvFileOption = Annotated[
    str,
    typer.Option("--env-file", help="Dotenv path when using --from-env"),
]
ApiTokenOption = Annotated[
    Optional[str],
    typer.Option("--api-token", help="HTB app API token"),
]
TokenOption = Annotated[
    Optional[str],
    typer.Option("--token", help="HTB app token (alias)"),
]
BearerOption = Annotated[
    Optional[str],
    typer.Option("--bearer", help="HTB bearer token (alias)"),
]

OPTION_HELP_EPILOG = """ Common options (use on ``pull`` or ``generate`` subcommands):

  -p, --profile ID       6-digit HTB profile ID
  -t, --template NAME    Badge template (generate only; default: classic)
  -o, --output-dir PATH  Badge output directory (generate only)
  --config PATH          Metrics YAML config (default: htb-metrics.yml)
  --no-cache             Disable API response cache
  --from-env             Load from .env (env wins over CLI/YAML)
  --env-file PATH        Dotenv file for --from-env (default: .env)
  --api-token TOKEN      HTB app API token
  --token TOKEN          HTB app token alias
  --bearer TOKEN         HTB bearer token alias
"""


def build_argv(
    *,
    profile: int | None = None,
    template: str | None = None,
    output_dir: str | None = None,
    config: str = "htb-metrics.yml",
    no_cache: bool = False,
    from_env: bool = False,
    env_file: str = ".env",
    api_token: str | None = None,
    token: str | None = None,
    bearer: str | None = None,
) -> list[str]:
    args: list[str] = []
    if from_env:
        args.append("--from-env")
    if env_file != ".env":
        args.extend(["--env-file", env_file])
    if profile is not None:
        args.extend(["-p", str(profile)])
    if template is not None:
        args.extend(["-t", template])
    if output_dir is not None:
        args.extend(["-o", output_dir])
    if config != "htb-metrics.yml":
        args.extend(["--config", config])
    if no_cache:
        args.append("--no-cache")
    if api_token:
        args.extend(["--api-token", api_token])
    if token:
        args.extend(["--token", token])
    if bearer:
        args.extend(["--bearer", bearer])
    return args
