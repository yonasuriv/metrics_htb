from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Settings:
    profile_id: int | None = None
    auth_token: str | None = None
    hide_banner: bool = False
    machine_info_img_cols: int = 31
    active_img_cols: int = 26
    metrics_template: str = "classic"
    metrics_cache_ttl: int = 3600
    metrics_hide_if_null: bool = True
    dashboard_port: int = 8080
    extra: dict = field(default_factory=dict)
