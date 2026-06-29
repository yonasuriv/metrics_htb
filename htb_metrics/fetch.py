from __future__ import annotations
import base64
import json
import time
from pathlib import Path
from typing import Any
import requests

API_V4 = "https://labs.hackthebox.com/api/v4"
API_V5 = "https://labs.hackthebox.com/api/v5"
API_EXP = "https://labs.hackthebox.com/api/experience/v1"
_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "htb-metrics/2.0",
}


class FetchError(Exception):
    pass


def _get(url: str) -> dict[str, Any]:
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=15)
    except requests.RequestException as e:
        raise FetchError(f"Request failed for {url}: {e}") from e
    if resp.status_code != 200:
        raise FetchError(f"HTTP {resp.status_code} from {url}")
    return resp.json()


def _cached_get(url: str, cache_path: Path, ttl: int) -> dict[str, Any]:
    if ttl > 0 and cache_path.exists():
        age = time.time() - cache_path.stat().st_mtime
        if age < ttl:
            return json.loads(cache_path.read_text())
    data = _get(url)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data, indent=2))
    return data


def _fetch_avatar_b64(url: str, cache_path: Path, ttl: int) -> str:
    if ttl > 0 and cache_path.exists():
        age = time.time() - cache_path.stat().st_mtime
        if age < ttl:
            return cache_path.read_text()
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=15)
        if resp.status_code == 200:
            mime = resp.headers.get("Content-Type", "image/png").split(";")[0]
            b64 = base64.b64encode(resp.content).decode("utf-8")
            data_uri = f"data:{mime};base64,{b64}"
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(data_uri)
            return data_uri
    except requests.RequestException as e:
        print(f"Warning: could not fetch avatar for b64: {e}")
    return url  # fallback to raw URL


def fetch_all(profile_id: int, cache_dir: str, cache_ttl: int) -> dict[str, Any]:
    base = Path(cache_dir) / str(profile_id)

    profile = _cached_get(
        f"{API_V4}/profile/{profile_id}",
        base / "profile.json",
        cache_ttl,
    )

    account_id: str | None = profile.get("profile", {}).get("account_id")
    if not account_id:
        raise FetchError(f"No account_id in profile response for {profile_id}")

    result: dict[str, Any] = {"profile": profile, "account_id": account_id}

    avatar_url = profile.get("profile", {}).get("avatar")
    if avatar_url:
        result["avatar_b64"] = _fetch_avatar_b64(
            avatar_url, base / "avatar_b64.txt", cache_ttl
        )

    secondary: dict[str, str] = {
        "user_machines": f"{API_V4}/profile/chart/machines/attack/{profile_id}",
        "user_os": f"{API_V4}/profile/progress/machines/os/{profile_id}",
        "user_challenges": f"{API_V4}/profile/progress/challenges/{profile_id}",
        "user_fortresses": f"{API_V4}/profile/progress/fortress/{profile_id}",
        "user_sherlocks": f"{API_V4}/profile/progress/sherlocks/{profile_id}",
        "user_prolabs": f"{API_V4}/profile/progress/prolab/{profile_id}",
        "user_activity": f"{API_V5}/user/profile/activity/{profile_id}?per_page=5",
        "season_ranks": f"{API_V4}/season/user/{profile_id}/ranks",
        "experience": f"{API_EXP}/account/{account_id}",
    }

    for name, url in secondary.items():
        try:
            result[name] = _cached_get(url, base / f"{name}.json", cache_ttl)
        except FetchError as e:
            print(f"Warning: could not fetch {name}: {e}")
            result[name] = None

    team = profile.get("profile", {}).get("team")
    team_id = team.get("id") if isinstance(team, dict) else None
    if team_id:
        for name, url in {
            "team": f"{API_V4}/public/team/info/{team_id}",
            "team_bracket": f"{API_V4}/public/rankings/team/ranking_bracket/{team_id}",
        }.items():
            try:
                result[name] = _cached_get(url, base / f"{name}.json", cache_ttl)
            except FetchError as e:
                print(f"Warning: could not fetch team {name}: {e}")
                result[name] = None

    return result
