import pytest
from htb_metrics.dataset import build_dataset

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
    "profile": {"activity": [{"date_diff": "2 days ago", "type": "machine"}]}
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
    assert ds["last_activity"] == "2 days ago"

def test_missing_experience_gives_none_not_crash():
    ds = build_dataset(make_raw(experience=None))
    assert ds.get("level_number") is None
    assert ds.get("level_title") is None

def test_missing_season_gives_none_not_crash():
    ds = build_dataset(make_raw(season_ranks=None))
    assert ds.get("season_league") is None

def test_empty_activity_gives_na():
    ds = build_dataset(make_raw(user_activity={"profile": {"activity": []}}))
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
