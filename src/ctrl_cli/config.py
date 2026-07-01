from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

from ctrl_config.auth import resolve_auth_token as _resolve_auth_token
from ctrl_config.paths import (
    CACHE_FILE,
    CONFIG_DIR,
    CONFIG_FILE,
    DEFAULT_CLI_CONFIG,
    DEFAULT_METRICS_CONFIG,
)

__all__ = [
    "CACHE_FILE",
    "CONFIG_DIR",
    "CONFIG_FILE",
    "DEFAULT_CLI_CONFIG",
    "DEFAULT_METRICS_CONFIG",
    "bootstrap_cli_config",
    "resolve_auth_token",
]


def resolve_auth_token(
    *,
    cli_api_token: str | None = None,
    cli_bearer: str | None = None,
    cli_config: str | None = None,
    metrics_config: str | None = None,
    from_env: bool = False,
) -> str | None:
    return _resolve_auth_token(
        cli_api_token=cli_api_token,
        cli_bearer=cli_bearer,
        cli_config=cli_config,
        metrics_config=metrics_config,
        json_config_file=CONFIG_FILE,
        from_env=from_env,
    )


def bootstrap_cli_config(
    *,
    from_env: bool = False,
    env_file: str = ".env",
    cli_config: str = DEFAULT_CLI_CONFIG,
    metrics_config: str = DEFAULT_METRICS_CONFIG,
    cli_api_token: str | None = None,
    cli_bearer: str | None = None,
) -> str | None:
    """Load dotenv/YAML and return a resolved bearer token, if any."""
    if from_env:
        env_path = Path(env_file)
        if not env_path.is_file():
            raise ValueError(
                f"--from-env requires {env_path}. "
                "Copy examples/config/.env.example to .env and fill in values."
            )
        load_dotenv(env_path, override=True)
    else:
        load_dotenv()

    return resolve_auth_token(
        cli_api_token=cli_api_token,
        cli_bearer=cli_bearer,
        cli_config=cli_config,
        metrics_config=metrics_config,
        from_env=from_env,
    )
