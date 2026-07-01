from __future__ import annotations
import os
import yaml
import argparse
from dataclasses import dataclass
from pathlib import Path

from htb_metrics.paths import TEMPLATES_DIR as _ASSETS
from htb_metrics.paths import default_cache_dir, default_output_dir


def _discover_templates() -> set[str]:
    names: set[str] = set()
    for p in (_ASSETS / "html").glob("*.html"):
        names.add(p.stem)
    for p in (_ASSETS / "svg").glob("*.svg"):
        names.add(p.stem)
    return names


VALID_TEMPLATES = _discover_templates()


def _env_bool(name: str) -> bool | None:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return None
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str) -> int | None:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return None
    return int(raw.strip())


def _first(*values):
    for value in values:
        if value is not None and value != "":
            return value
    return None


@dataclass
class Config:
    profile_id: int
    template: str = "classic"
    output_dir: str = ""
    cache_ttl: int = 3600
    hide_if_null: bool = True
    cache_dir: str = ""
    auth_token: str | None = None

    def validate(self) -> None:
        id_str = str(self.profile_id)
        if not (len(id_str) == 6 and id_str.isdigit()):
            raise ValueError(f"profile_id must be a 6-digit number, got: {self.profile_id}")
        if self.template not in VALID_TEMPLATES:
            raise ValueError(
                f"template must be one of {sorted(VALID_TEMPLATES)}, got: {self.template}"
            )


def resolve_auth_token(
    *,
    cli_api_token: str | None = None,
    cli_token: str | None = None,
    cli_bearer: str | None = None,
    file_cfg: dict | None = None,
    from_env: bool = False,
) -> str | None:
    """Resolve HTB API bearer token from CLI, env, or config file."""
    file_cfg = file_cfg or {}
    env_api = os.environ.get("HTB_API_TOKEN")
    env_token = os.environ.get("HTB_TOKEN")
    env_bearer = os.environ.get("HTB_BEARER")

    if from_env:
        order = (
            env_api,
            env_token,
            env_bearer,
            cli_api_token,
            cli_token,
            cli_bearer,
            file_cfg.get("api_token"),
            file_cfg.get("token"),
            file_cfg.get("bearer"),
        )
    else:
        order = (
            cli_api_token,
            cli_token,
            cli_bearer,
            env_api,
            env_token,
            env_bearer,
            file_cfg.get("api_token"),
            file_cfg.get("token"),
            file_cfg.get("bearer"),
        )

    for value in order:
        if value:
            return str(value).strip()
    return None


def load_config(args: list[str] | None = None) -> Config:
    """Load config.

    Default priority: CLI flags > env vars > config file > defaults.
    With ``--from-env``: env vars > CLI flags > config file > defaults
    (after loading ``--env-file``, default ``.env``).
    """
    from dotenv import load_dotenv

    parser = argparse.ArgumentParser(description="HTB Metrics Generator", add_help=True)
    parser.add_argument("-p", "--profile", type=int, default=None)
    parser.add_argument("-t", "--template", type=str, default=None)
    parser.add_argument("-o", "--output-dir", type=str, default=None)
    parser.add_argument("--config", type=str, default="htb-metrics.yml")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--api-token", type=str, default=None, help="HTB app API token")
    parser.add_argument("--token", type=str, default=None, help="HTB app token (alias)")
    parser.add_argument("--bearer", type=str, default=None, help="HTB bearer token (alias)")
    parser.add_argument(
        "--from-env",
        action="store_true",
        help="Load settings from environment / .env (env wins over CLI and yaml)",
    )
    parser.add_argument(
        "--env-file",
        type=str,
        default=".env",
        help="Dotenv file to load when using --from-env (default: .env)",
    )
    parsed = parser.parse_args(args)

    if parsed.from_env:
        env_path = Path(parsed.env_file)
        if not env_path.exists():
            raise ValueError(
                f"--from-env requires {env_path}. "
                "Copy examples/config/.env.example to .env and fill in values."
            )
        load_dotenv(env_path, override=True)
    else:
        load_dotenv()

    file_cfg: dict = {}
    config_path = Path(parsed.config)
    if config_path.exists():
        with config_path.open() as f:
            file_cfg = yaml.safe_load(f) or {}

    env_profile = _env_int("HTB_PROFILE_ID")
    env_template = os.environ.get("HTB_TEMPLATE")
    env_output = os.environ.get("HTB_OUTPUT_DIR")
    env_cache_dir = os.environ.get("HTB_CACHE_DIR")
    env_cache_ttl = _env_int("HTB_CACHE_TTL")
    env_hide_if_null = _env_bool("HTB_HIDE_IF_NULL")
    env_no_cache = _env_bool("HTB_NO_CACHE")

    if parsed.from_env:
        profile_id = _first(env_profile, parsed.profile, file_cfg.get("profile_id"))
        template = _first(env_template, parsed.template, file_cfg.get("template"), "classic")
    else:
        profile_id = _first(parsed.profile, env_profile, file_cfg.get("profile_id"))
        template = _first(parsed.template, env_template, file_cfg.get("template"), "classic")

    if not profile_id:
        raise ValueError(
            "Profile ID is required. Use -p/--profile, HTB_PROFILE_ID env var, "
            "or profile_id in htb-metrics.yml"
        )

    profile_id = int(profile_id)
    default_data = default_cache_dir(profile_id)
    default_badges = default_output_dir(profile_id)

    if parsed.from_env:
        output_dir = _first(env_output, parsed.output_dir, file_cfg.get("output_dir"), default_badges)
        cache_dir = _first(env_cache_dir, file_cfg.get("cache_dir"), default_data)
        if env_no_cache is True:
            cache_ttl = 0
        elif parsed.no_cache:
            cache_ttl = 0
        else:
            cache_ttl = _first(env_cache_ttl, file_cfg.get("cache_ttl"), 3600)
        hide_if_null = (
            env_hide_if_null
            if env_hide_if_null is not None
            else bool(file_cfg.get("hide_if_null", True))
        )
    else:
        output_dir = _first(parsed.output_dir, env_output, file_cfg.get("output_dir"), default_badges)
        cache_dir = _first(env_cache_dir, file_cfg.get("cache_dir"), default_data)
        if parsed.no_cache or env_no_cache is True:
            cache_ttl = 0
        else:
            cache_ttl = _first(env_cache_ttl, file_cfg.get("cache_ttl"), 3600)
        hide_if_null = (
            env_hide_if_null
            if env_hide_if_null is not None
            else bool(file_cfg.get("hide_if_null", True))
        )

    cfg = Config(
        profile_id=profile_id,
        template=str(template),
        output_dir=str(output_dir),
        cache_ttl=int(cache_ttl),
        hide_if_null=bool(hide_if_null),
        cache_dir=str(cache_dir),
        auth_token=resolve_auth_token(
            cli_api_token=parsed.api_token,
            cli_token=parsed.token,
            cli_bearer=parsed.bearer,
            file_cfg=file_cfg,
            from_env=parsed.from_env,
        ),
    )
    cfg.validate()
    return cfg
