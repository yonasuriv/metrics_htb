import json
import time
import pytest
import responses as resp_lib
from pathlib import Path
from htb_metrics.fetch import fetch_all, FetchError

PROFILE_URL = "https://labs.hackthebox.com/api/v4/profile/780424"
SEASON_URL = "https://labs.hackthebox.com/api/v4/season/user/780424/ranks"
EXP_URL = "https://labs.hackthebox.com/api/experience/v1/account/abc-123"

PROFILE_BODY = {
    "profile": {
        "id": 780424,
        "account_id": "abc-123",
        "name": "testuser",
        "rank": "Pro Hacker",
        "avatar": "https://example.com/avatar.png",
        "user_owns": 61,
        "system_owns": 53,
        "ranking": 914,
        "points": 121,
        "respects": 1,
        "team": None,
    }
}
SEASON_BODY = {
    "data": [{"league": "Ruby", "rank": 274, "season_name": "Season 11",
               "rank_suffix": "th", "total_season_points": 350}]
}
EXP_BODY = {
    "level": 76, "levelTitle": "Prodigy", "levelGrade": "1",
    "rankImage": "https://example.com/rank.svg",
    "rankImageBackground": "https://example.com/bg.svg",
    "totalExperiencePoints": 85575,
}

def _stub_all(rsps):
    rsps.add(resp_lib.GET, PROFILE_URL, json=PROFILE_BODY, status=200)
    rsps.add(resp_lib.GET, SEASON_URL, json=SEASON_BODY, status=200)
    rsps.add(resp_lib.GET, EXP_URL, json=EXP_BODY, status=200)
    for path in ["machines/attack", "machines/os", "challenges", "fortress",
                 "sherlocks", "prolab", "activity"]:
        rsps.add(resp_lib.GET,
                 f"https://labs.hackthebox.com/api/v4/profile/progress/{path}/780424",
                 json={}, status=200)
    rsps.add(resp_lib.GET,
             "https://labs.hackthebox.com/api/v4/profile/chart/machines/attack/780424",
             json={}, status=200)
    rsps.add(resp_lib.GET,
             "https://labs.hackthebox.com/api/v4/profile/activity/780424",
             json={}, status=200)

@resp_lib.activate
def test_fetch_all_returns_profile_and_experience(tmp_path):
    _stub_all(resp_lib)
    result = fetch_all(780424, str(tmp_path), cache_ttl=0)
    assert result["account_id"] == "abc-123"
    assert result["profile"]["profile"]["name"] == "testuser"
    assert result["experience"]["level"] == 76
    assert result["season_ranks"]["data"][0]["league"] == "Ruby"

@resp_lib.activate
def test_fetch_caches_to_disk(tmp_path):
    _stub_all(resp_lib)
    fetch_all(780424, str(tmp_path), cache_ttl=3600)
    cache_file = tmp_path / "780424" / "profile.json"
    assert cache_file.exists()
    data = json.loads(cache_file.read_text())
    assert data["profile"]["name"] == "testuser"

@resp_lib.activate
def test_fetch_uses_cache_within_ttl(tmp_path):
    _stub_all(resp_lib)
    fetch_all(780424, str(tmp_path), cache_ttl=3600)
    call_count_after_first = len(resp_lib.calls)
    # Second call — should not add HTTP calls for cached endpoints
    fetch_all(780424, str(tmp_path), cache_ttl=3600)
    assert len(resp_lib.calls) == call_count_after_first

@resp_lib.activate
def test_secondary_endpoint_failure_is_non_fatal(tmp_path):
    resp_lib.add(resp_lib.GET, PROFILE_URL, json=PROFILE_BODY, status=200)
    resp_lib.add(resp_lib.GET, SEASON_URL, status=500)
    resp_lib.add(resp_lib.GET, EXP_URL, json=EXP_BODY, status=200)
    for path in ["machines/attack", "machines/os", "challenges", "fortress",
                 "sherlocks", "prolab"]:
        resp_lib.add(resp_lib.GET,
                     f"https://labs.hackthebox.com/api/v4/profile/progress/{path}/780424",
                     json={}, status=200)
    resp_lib.add(resp_lib.GET,
                 "https://labs.hackthebox.com/api/v4/profile/chart/machines/attack/780424",
                 json={}, status=200)
    resp_lib.add(resp_lib.GET,
                 "https://labs.hackthebox.com/api/v4/profile/activity/780424",
                 json={}, status=200)
    result = fetch_all(780424, str(tmp_path), cache_ttl=0)
    assert result["season_ranks"] is None

@resp_lib.activate
def test_private_profile_raises_fetch_error(tmp_path):
    resp_lib.add(resp_lib.GET, PROFILE_URL, status=403)
    with pytest.raises(FetchError, match="HTTP 403"):
        fetch_all(780424, str(tmp_path), cache_ttl=0)
