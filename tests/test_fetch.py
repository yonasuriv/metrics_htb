import json
import pytest
import responses as resp_lib
from pathlib import Path
from htb_metrics.fetch import fetch_all, FetchError

PROFILE_ID = 780424
PROFILE_URL = f"https://labs.hackthebox.com/api/v4/profile/{PROFILE_ID}"
SEASON_URL = f"https://labs.hackthebox.com/api/v4/season/user/{PROFILE_ID}/ranks"
EXP_URL = "https://labs.hackthebox.com/api/experience/v1/account/abc-123"
ACTIVITY_URL = (
    f"https://labs.hackthebox.com/api/v5/user/profile/activity/{PROFILE_ID}?per_page=5"
)
MACHINES_URL = "https://labs.hackthebox.com/api/v5/machines/"
TRACKS_URL = "https://labs.hackthebox.com/api/v5/tracks/"
RANKINGS_URL = "https://labs.hackthebox.com/api/v4/rankings"

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


def _stub_public(rsps, profile_body=None):
    body = profile_body or PROFILE_BODY
    rsps.add(resp_lib.GET, PROFILE_URL, json=body, status=200)
    rsps.add(resp_lib.GET, SEASON_URL, json=SEASON_BODY, status=200)
    rsps.add(resp_lib.GET, EXP_URL, json=EXP_BODY, status=200)
    rsps.add(resp_lib.GET, ACTIVITY_URL, json={"data": []}, status=200)
    for path in ["machines", "challenges", "fortress", "sherlocks", "prolab"]:
        rsps.add(
            resp_lib.GET,
            f"https://labs.hackthebox.com/api/v4/profile/progress/{path}/{PROFILE_ID}",
            json={},
            status=200,
        )
    avatar_url = body["profile"]["avatar"]
    rsps.add(resp_lib.GET, avatar_url, body=b"avatar", status=200,
             headers={"Content-Type": "image/png"})


@resp_lib.activate
def test_fetch_all_returns_profile_and_experience(tmp_path):
    _stub_public(resp_lib)
    result = fetch_all(780424, str(tmp_path), cache_ttl=0)
    assert result["account_id"] == "abc-123"
    assert result["profile"]["profile"]["name"] == "testuser"
    assert result["experience"]["level"] == 76
    assert result["season_ranks"]["data"][0]["league"] == "Ruby"
    assert "machines" not in result
    assert "user_tracks" not in result
    assert "team_rankings" not in result


@resp_lib.activate
def test_fetch_caches_to_disk(tmp_path):
    _stub_public(resp_lib)
    fetch_all(780424, str(tmp_path), cache_ttl=3600)
    cache_file = tmp_path / "780424" / "profile.json"
    assert cache_file.exists()
    data = json.loads(cache_file.read_text())
    assert data["profile"]["name"] == "testuser"


@resp_lib.activate
def test_fetch_uses_cache_within_ttl(tmp_path):
    _stub_public(resp_lib)
    fetch_all(780424, str(tmp_path), cache_ttl=3600)
    call_count_after_first = len(resp_lib.calls)
    fetch_all(780424, str(tmp_path), cache_ttl=3600)
    assert len(resp_lib.calls) == call_count_after_first


@resp_lib.activate
def test_secondary_endpoint_failure_is_non_fatal(tmp_path):
    resp_lib.add(resp_lib.GET, PROFILE_URL, json=PROFILE_BODY, status=200)
    resp_lib.add(resp_lib.GET, SEASON_URL, status=500)
    resp_lib.add(resp_lib.GET, EXP_URL, json=EXP_BODY, status=200)
    resp_lib.add(resp_lib.GET, ACTIVITY_URL, json={"data": []}, status=200)
    for path in ["machines", "challenges", "fortress", "sherlocks", "prolab"]:
        resp_lib.add(
            resp_lib.GET,
            f"https://labs.hackthebox.com/api/v4/profile/progress/{path}/{PROFILE_ID}",
            json={},
            status=200,
        )
    result = fetch_all(780424, str(tmp_path), cache_ttl=0)
    assert result["season_ranks"] is None


@resp_lib.activate
def test_auth_endpoints_fetched_with_token(tmp_path):
    _stub_public(resp_lib)
    resp_lib.add(resp_lib.GET, MACHINES_URL, json={"data": []}, status=200)
    resp_lib.add(resp_lib.GET, TRACKS_URL, json={"data": []}, status=200)
    resp_lib.add(resp_lib.GET, RANKINGS_URL, json={"data": {}}, status=200)

    result = fetch_all(780424, str(tmp_path), cache_ttl=0, auth_token="test-token")
    assert result["machines"] == {"data": []}
    assert result["user_tracks"] == {"data": []}
    assert result["team_rankings"] == {"data": {}}

    auth_calls = [
        call for call in resp_lib.calls
        if call.request.headers.get("Authorization") == "Bearer test-token"
    ]
    assert len(auth_calls) == 3


@resp_lib.activate
def test_private_profile_raises_fetch_error(tmp_path):
    resp_lib.add(resp_lib.GET, PROFILE_URL, status=403)
    with pytest.raises(FetchError, match="HTTP 403"):
        fetch_all(780424, str(tmp_path), cache_ttl=0)
