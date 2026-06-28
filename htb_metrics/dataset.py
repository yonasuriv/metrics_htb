from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


def build_dataset(raw: dict[str, Any]) -> dict[str, Any]:
    ds: dict[str, Any] = {}

    # --- Profile (legacy rank, core identity) ---
    p = raw.get("profile", {}).get("profile", {})
    ds["user_name"] = p.get("name")
    ds["user_rank"] = p.get("rank")
    ds["user_avatar"] = p.get("avatar")
    ds["user_owns"] = p.get("user_owns")
    ds["user_system_owns"] = p.get("system_owns")
    ds["user_ranking"] = p.get("ranking")
    ds["user_points"] = p.get("points")
    ds["user_respects"] = p.get("respects")
    ds["user_bloods"] = p.get("user_bloods")
    ds["user_system_bloods"] = p.get("system_bloods")
    ds["user_challenge_bloods"] = p.get("challenge_bloods")
    ds["user_country"] = p.get("country_name")
    ds["account_id"] = raw.get("account_id")

    # --- Experience (new level system) ---
    exp = raw.get("experience") or {}
    ds["level_number"] = exp.get("level")
    ds["level_title"] = exp.get("levelTitle")
    ds["level_grade"] = exp.get("levelGrade")
    ds["level_image_url"] = exp.get("rankImage")
    ds["level_bg_url"] = exp.get("rankImageBackground")
    ds["level_xp_total"] = exp.get("totalExperiencePoints")
    ds["level_streak"] = (exp.get("streak") or {}).get("counter")

    # --- Season (current league + rank) ---
    season_raw = raw.get("season_ranks") or {}
    seasons = season_raw.get("data", []) if isinstance(season_raw, dict) else []
    if seasons:
        s = seasons[0]
        ds["season_name"] = s.get("season_name")
        ds["season_league"] = s.get("league")
        ds["season_rank"] = s.get("rank")
        ds["season_rank_suffix"] = s.get("rank_suffix")
        ds["season_points"] = s.get("total_season_points")
        flags = s.get("total_season_flags") or {}
        ds["season_flags_obtained"] = flags.get("obtained")
        ds["season_flags_total"] = flags.get("total")

    # --- Activity ---
    activity_raw = raw.get("user_activity") or {}
    activities = activity_raw.get("profile", {}).get("activity", [])
    ds["last_activity"] = activities[0].get("date_diff", "N/A") if activities else "N/A"

    # --- Team ---
    team = p.get("team")
    if isinstance(team, dict):
        ds["team_name"] = team.get("name")
        ds["team_id"] = team.get("id")
        ds["team_ranking"] = team.get("ranking")

    # --- Metadata ---
    ds["last_update"] = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    return ds
