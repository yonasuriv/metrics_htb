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
    ds["user_avatar_b64"] = raw.get("avatar_b64") or p.get("avatar")
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

    # --- Activity (v5 API: data[].ownDate ISO timestamp) ---
    activity_raw = raw.get("user_activity") or {}
    activities = activity_raw.get("data", [])
    if activities and activities[0].get("ownDate"):
        try:
            dt = datetime.fromisoformat(activities[0]["ownDate"].replace("Z", "+00:00"))
            ds["last_activity"] = dt.strftime("%d %b %Y")
        except (ValueError, KeyError):
            ds["last_activity"] = "N/A"
    else:
        ds["last_activity"] = "N/A"

    # --- Team ---
    team = p.get("team")
    if isinstance(team, dict):
        ds["team_name"] = team.get("name")
        ds["team_id"] = team.get("id")
        ds["team_ranking"] = team.get("ranking")
        thumb = team.get("logo_thumb_url") or ""
        ds["team_avatar"] = thumb.replace("_thumb.", ".") if thumb else None

    # --- Metadata ---
    ds["last_update"] = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")

    # --- Computed bar widths (capped 0–100 for CSS width%) ---
    def _pct(val, max_val):
        if val is None:
            return 0
        return min(int(val * 100 / max_val), 100)

    ds["user_owns_bar_pct"] = _pct(ds.get("user_owns"), 200)
    ds["user_system_owns_bar_pct"] = _pct(ds.get("user_system_owns"), 200)
    ds["season_points_bar_pct"] = _pct(ds.get("season_points"), 2000)
    ds["level_xp_bar_pct"] = _pct(ds.get("level_xp_total"), 150000)

    return ds
