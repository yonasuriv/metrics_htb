from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

from ctrl_config.paths import CONFIG_FILE, DEFAULT_CLI_CONFIG, DEFAULT_METRICS_CONFIG


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


def _load_json_config(config_file: Path | None = None) -> dict:
    path = config_file or CONFIG_FILE
    if not path.is_file():
        return {}
    try:
        with path.open() as handle:
            return json.load(handle)
    except json.JSONDecodeError:
        return {}


def _yaml_auth_tokens(*cfgs: dict) -> tuple:
    tokens = []
    for cfg in cfgs:
        tokens.extend((cfg.get("api_token"), cfg.get("token"), cfg.get("bearer")))
        auth = cfg.get("auth")
        if isinstance(auth, dict):
            tokens.extend((auth.get("api_token"), auth.get("token"), auth.get("bearer")))
    return tuple(tokens)


def resolve_auth_token(
    *,
    cli_api_token: str | None = None,
    cli_token: str | None = None,
    cli_bearer: str | None = None,
    cli_config: str | Path | None = None,
    metrics_config: str | Path | None = None,
    unified_config: str | Path | None = None,
    file_cfg: dict | None = None,
    json_config_file: Path | None = None,
    from_env: bool = False,
) -> str | None:
    """Resolve HTB API bearer token from CLI, env, YAML, or saved JSON."""
    unified_cfg = _load_yaml(Path(unified_config)) if unified_config else {}
    cli_cfg = _load_yaml(Path(cli_config or DEFAULT_CLI_CONFIG))
    metrics_cfg = _load_yaml(Path(metrics_config or DEFAULT_METRICS_CONFIG))
    inline_cfg = file_cfg or {}
    json_cfg = _load_json_config(json_config_file)

    env_api = os.environ.get("HTB_API_TOKEN")
    env_token = os.environ.get("HTB_TOKEN")
    env_bearer = os.environ.get("HTB_BEARER")

    yaml_tokens = _yaml_auth_tokens(unified_cfg, cli_cfg, metrics_cfg, inline_cfg)
    json_token = json_cfg.get("token")

    cli_tokens = (cli_api_token, cli_token, cli_bearer)
    env_tokens = (env_api, env_token, env_bearer)

    if from_env:
        order = (*env_tokens, *cli_tokens, *yaml_tokens, json_token)
    else:
        order = (*cli_tokens, *env_tokens, *yaml_tokens, json_token)

    for value in order:
        if value:
            return str(value).strip()
    return None
