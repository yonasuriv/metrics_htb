from __future__ import annotations

import json
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

CONFIG_DIR = Path.home() / ".config" / "htbcli"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_CLI_CONFIG = "htb-cli.yml"
DEFAULT_METRICS_CONFIG = "htb-metrics.yml"


def _first(*values):
    for value in values:
        if value is not None and value != "":
            return value
    return None


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    with path.open() as handle:
        return yaml.safe_load(handle) or {}


def _load_json_config() -> dict:
    if not CONFIG_FILE.is_file():
        return {}
    try:
        with CONFIG_FILE.open() as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return {}


def resolve_auth_token(
    *,
    cli_api_token: str | None = None,
    cli_bearer: str | None = None,
    cli_config: str | None = None,
    metrics_config: str | None = None,
    from_env: bool = False,
) -> str | None:
    """Resolve HTB API bearer token from CLI, env, YAML, or ~/.config/htbcli."""
    cli_cfg = _load_yaml(Path(cli_config or DEFAULT_CLI_CONFIG))
    metrics_cfg = _load_yaml(Path(metrics_config or DEFAULT_METRICS_CONFIG))
    json_cfg = _load_json_config()

    env_api = os.environ.get("HTB_API_TOKEN")
    env_token = os.environ.get("HTB_TOKEN")
    env_bearer = os.environ.get("HTB_BEARER")

    yaml_tokens = (
        cli_cfg.get("api_token"),
        cli_cfg.get("token"),
        cli_cfg.get("bearer"),
        metrics_cfg.get("api_token"),
        metrics_cfg.get("token"),
        metrics_cfg.get("bearer"),
    )
    json_token = json_cfg.get("token")

    if from_env:
        order = (
            env_api,
            env_token,
            env_bearer,
            cli_api_token,
            cli_bearer,
            *yaml_tokens,
            json_token,
        )
    else:
        order = (
            cli_api_token,
            cli_bearer,
            env_api,
            env_token,
            env_bearer,
            *yaml_tokens,
            json_token,
        )

    for value in order:
        if value:
            return str(value).strip()
    return None


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
