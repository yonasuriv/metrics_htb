from __future__ import annotations
import os
import yaml
import argparse
from dataclasses import dataclass
from pathlib import Path

VALID_TEMPLATES = {
    "classic", "compact", "profile-card", "rank-card",
    "season-card", "terminal", "hacker-red", "hacker-yellow",
    "light", "minimal",
}

@dataclass
class Config:
    profile_id: int
    template: str = "classic"
    output_dir: str = "output"
    cache_ttl: int = 3600
    hide_if_null: bool = True
    cache_dir: str = ".cache"

    def validate(self) -> None:
        id_str = str(self.profile_id)
        if not (len(id_str) == 6 and id_str.isdigit()):
            raise ValueError(f"profile_id must be a 6-digit number, got: {self.profile_id}")
        if self.template not in VALID_TEMPLATES:
            raise ValueError(
                f"template must be one of {sorted(VALID_TEMPLATES)}, got: {self.template}"
            )


def load_config(args: list[str] | None = None) -> Config:
    """Priority: CLI args > env vars > config file > defaults."""
    parser = argparse.ArgumentParser(description="HTB Metrics Generator", add_help=True)
    parser.add_argument("-p", "--profile", type=int, default=None)
    parser.add_argument("-t", "--template", type=str, default=None)
    parser.add_argument("-o", "--output-dir", type=str, default=None)
    parser.add_argument("--config", type=str, default="htb-metrics.yml")
    parser.add_argument("--no-cache", action="store_true")
    parsed = parser.parse_args(args)

    file_cfg: dict = {}
    config_path = Path(parsed.config)
    if config_path.exists():
        with config_path.open() as f:
            file_cfg = yaml.safe_load(f) or {}

    profile_id = (
        parsed.profile
        or (int(os.environ["HTB_PROFILE_ID"]) if "HTB_PROFILE_ID" in os.environ else None)
        or file_cfg.get("profile_id")
    )
    if not profile_id:
        raise ValueError(
            "Profile ID is required. Use -p/--profile, HTB_PROFILE_ID env var, "
            "or profile_id in htb-metrics.yml"
        )

    cfg = Config(
        profile_id=int(profile_id),
        template=(
            parsed.template
            or os.environ.get("HTB_TEMPLATE")
            or file_cfg.get("template", "classic")
        ),
        output_dir=(
            parsed.output_dir
            or os.environ.get("HTB_OUTPUT_DIR")
            or file_cfg.get("output_dir", "output")
        ),
        cache_ttl=0 if parsed.no_cache else int(file_cfg.get("cache_ttl", 3600)),
        hide_if_null=bool(file_cfg.get("hide_if_null", True)),
        cache_dir=file_cfg.get("cache_dir", ".cache"),
    )
    cfg.validate()
    return cfg
