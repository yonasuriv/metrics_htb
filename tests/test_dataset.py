import pytest
from ctrl_metrics.dataset import build_dataset

PROFILE_BODY = {
    "profile": {
        "id": 780424,
        "account_id": "abc-123",
        "name": "testuser",
        "rank": "Pro Hacker",
        "avatar": "https://example.com/avatar.png",
        "user_owns": 61,
        "system_owns": 53,
        "user_bloods": 2,
        "system_bloods": 1,
        "ranking": 914,
        "points": 121,
        "respects": 1,
        "team": None,
    }
}
EXP_BODY = {
    "level": 76, "levelTitle": "Prodigy", "levelGrade": "1",
    "rankImage": "https://example.com/rank.svg",
    "rankImageBackground": "https://example.com/bg.svg",
    "totalExperiencePoints": 85575,
}
SEASON_BODY = {
    "data": [{"league": "Ruby", "rank": 274, "season_name": "Season 11",
               "rank_suffix": "th", "total_season_points": 350}]
}
ACTIVITY_BODY = {
    "data": [{"type": "root", "name": "Enigma", "ownDate": "2026-06-27T20:31:45.000Z"}]
}

def make_raw(**overrides):
    base = {
        "profile": PROFILE_BODY,
        "account_id": "abc-123",
        "experience": EXP_BODY,
        "season_ranks": SEASON_BODY,
        "user_activity": ACTIVITY_BODY,
    }
    base.update(overrides)
    return base

def test_basic_profile_fields():
    ds = build_dataset(make_raw())
    assert ds["user_name"] == "testuser"
    assert ds["user_rank"] == "Pro Hacker"
    assert ds["user_owns"] == 61
    assert ds["user_system_owns"] == 53
    assert ds["user_ranking"] == 914
    assert ds["user_points"] == 121
    assert ds["user_respects"] == 1

def test_experience_fields():
    ds = build_dataset(make_raw())
    assert ds["level_number"] == 76
    assert ds["level_title"] == "Prodigy"
    assert ds["level_grade"] == "1"
    assert ds["level_xp_total"] == 85575

def test_season_fields():
    ds = build_dataset(make_raw())
    assert ds["season_league"] == "Ruby"
    assert ds["season_rank"] == 274
    assert ds["season_name"] == "Season 11"
    assert ds["season_points"] == 350

def test_activity_last_activity():
    ds = build_dataset(make_raw())
    assert ds["last_activity"] == "27 Jun 2026"

def test_missing_experience_gives_none_not_crash():
    ds = build_dataset(make_raw(experience=None))
    assert ds.get("level_number") is None
    assert ds.get("level_title") is None

def test_missing_season_gives_none_not_crash():
    ds = build_dataset(make_raw(season_ranks=None))
    assert ds.get("season_league") is None

def test_empty_activity_gives_na():
    ds = build_dataset(make_raw(user_activity={"data": []}))
    assert ds["last_activity"] == "N/A"

def test_no_activity_endpoint_gives_na():
    ds = build_dataset(make_raw(user_activity=None))
    assert ds["last_activity"] == "N/A"

def test_last_update_is_set():
    ds = build_dataset(make_raw())
    assert "last_update" in ds
    assert "UTC" in ds["last_update"]

def test_account_id_present():
    ds = build_dataset(make_raw())
    assert ds["account_id"] == "abc-123"


# --- bar_pct computed fields ---

def test_user_owns_bar_pct():
    # 61 owns out of max 200 → int(61 * 100 / 200) = 30
    ds = build_dataset(make_raw())
    assert ds["user_owns_bar_pct"] == 30

def test_user_system_owns_bar_pct():
    # 53 owns out of max 200 → int(53 * 100 / 200) = 26
    ds = build_dataset(make_raw())
    assert ds["user_system_owns_bar_pct"] == 26

def test_season_points_bar_pct():
    # 350 points out of max 2000 → int(350 * 100 / 2000) = 17
    ds = build_dataset(make_raw())
    assert ds["season_points_bar_pct"] == 17

def test_level_xp_bar_pct():
    # 85575 XP out of max 150000 → int(85575 * 100 / 150000) = 57
    ds = build_dataset(make_raw())
    assert ds["level_xp_bar_pct"] == 57

def test_bar_pct_none_returns_zero():
    # With no experience data, level_xp_total is None → bar_pct should be 0
    ds = build_dataset(make_raw(experience=None))
    assert ds["level_xp_bar_pct"] == 0
    # With no season data, season_points is not set → bar_pct should be 0
    ds2 = build_dataset(make_raw(season_ranks=None))
    assert ds2["season_points_bar_pct"] == 0

def test_bar_pct_capped_at_100():
    import copy
    # Set user_owns to 300, which exceeds max_val of 200 → should be capped at 100
    profile_body = copy.deepcopy(PROFILE_BODY)
    profile_body["profile"]["user_owns"] = 300
    ds = build_dataset(make_raw(profile=profile_body))
    assert ds["user_owns_bar_pct"] == 100
