from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from ctrl_config.auth import resolve_auth_token
from ctrl_config.paths import (
    DEFAULT_CLI_CONFIG,
    DEFAULT_METRICS_CONFIG,
    REPO_CONFIG,
    USER_CONFIG,
)
from ctrl_config.schema import Settings


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


def _section(cfg: dict, name: str) -> dict:
    block = cfg.get(name)
    return block if isinstance(block, dict) else {}


def load_settings(
    *,
    from_env: bool = False,
    env_file: str = ".env",
    config_paths: list[Path | str] | None = None,
    cli_api_token: str | None = None,
    cli_bearer: str | None = None,
    cli_profile: int | None = None,
) -> Settings:
    """Load unified settings with SSOT priority.

    CLI flags > env > repo htb-ctrl.yml > ~/.config/htb-ctrl/config.yml
    > legacy htb-cli.yml / htb-metrics.yml > defaults.
    With ``from_env``: env wins over CLI flags (after loading env_file).
    """
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

    paths = [Path(p) for p in (config_paths or [])]
    if not paths:
        paths = [REPO_CONFIG, USER_CONFIG, Path(DEFAULT_CLI_CONFIG), Path(DEFAULT_METRICS_CONFIG)]

    merged: dict = {}
    for path in reversed(paths):
        merged = {**_load_yaml(path), **merged}

    cli_section = _section(merged, "cli")
    metrics_section = _section(merged, "metrics")
    auth_section = _section(merged, "auth")
    dashboard_section = _section(merged, "dashboard")

    env_profile = os.environ.get("HTB_PROFILE_ID")
    env_template = os.environ.get("HTB_TEMPLATE")
    env_hide_banner = os.environ.get("HTB_HIDE_BANNER")

    if from_env:
        profile_id = _first(env_profile, cli_profile, merged.get("profile_id"), metrics_section.get("profile_id"))
    else:
        profile_id = _first(cli_profile, env_profile, merged.get("profile_id"), metrics_section.get("profile_id"))

    hide_banner_raw = _first(
        cli_section.get("hide_banner"),
        merged.get("hide_banner"),
        env_hide_banner,
        False,
    )
    hide_banner = str(hide_banner_raw).strip().lower() in ("1", "true", "yes", "on")

    auth_token = resolve_auth_token(
        cli_api_token=cli_api_token,
        cli_bearer=cli_bearer,
        unified_config=paths[0] if paths else None,
        cli_config=DEFAULT_CLI_CONFIG,
        metrics_config=DEFAULT_METRICS_CONFIG,
        file_cfg={**merged, **auth_section},
        from_env=from_env,
    )

    return Settings(
        profile_id=int(profile_id) if profile_id not in (None, "") else None,
        auth_token=auth_token,
        hide_banner=hide_banner,
        machine_info_img_cols=int(cli_section.get("machine_info_img_cols", 31)),
        active_img_cols=int(cli_section.get("active_img_cols", 26)),
        metrics_template=str(_first(env_template, metrics_section.get("template"), merged.get("template"), "classic")),
        metrics_cache_ttl=int(metrics_section.get("cache_ttl", merged.get("cache_ttl", 3600))),
        metrics_hide_if_null=bool(metrics_section.get("hide_if_null", merged.get("hide_if_null", True))),
        dashboard_port=int(dashboard_section.get("default_port", 8080)),
        extra=merged,
    )
