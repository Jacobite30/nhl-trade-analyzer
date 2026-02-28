"""NHL API client for fetching live player and roster data.

Uses the free NHL API (api-web.nhle.com) which requires no authentication.
"""

import threading
from datetime import date
from urllib.request import urlopen, Request
from urllib.error import URLError
import json

from src.nhl_data import NHL_TEAMS


NHL_API_BASE = "https://api-web.nhle.com/v1"

# Position code mapping from NHL API codes to display names
POSITION_MAP = {
    "C": "C",
    "L": "LW",
    "R": "RW",
    "D": "D",
    "G": "G",
}


def _api_get(url, timeout=10):
    """Make a GET request to the NHL API and return parsed JSON."""
    req = Request(url, headers={"User-Agent": "NHL-Trade-Analyzer/1.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (URLError, json.JSONDecodeError, OSError):
        return None


def _calculate_age(birth_date_str):
    """Calculate age from a birth date string (YYYY-MM-DD)."""
    try:
        birth = date.fromisoformat(birth_date_str)
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return str(age)
    except (ValueError, TypeError):
        return ""


def _get_current_season():
    """Return current NHL season string (e.g. '20252026')."""
    today = date.today()
    if today.month >= 9:
        return f"{today.year}{today.year + 1}"
    else:
        return f"{today.year - 1}{today.year}"


def fetch_team_roster(team_abbr, season=None):
    """
    Fetch the roster for a team.

    Returns a list of player dicts with keys:
        id, name, position, age, birth_date
    """
    if season is None:
        season = _get_current_season()

    url = f"{NHL_API_BASE}/roster/{team_abbr}/{season}"
    data = _api_get(url)
    if not data:
        return []

    players = []
    for group in ["forwards", "defensemen", "goalies"]:
        for p in data.get(group, []):
            first = p.get("firstName", {}).get("default", "")
            last = p.get("lastName", {}).get("default", "")
            pos_code = p.get("positionCode", "")
            position = POSITION_MAP.get(pos_code, pos_code)
            birth_date = p.get("birthDate", "")
            age = _calculate_age(birth_date)

            players.append({
                "id": p.get("id", 0),
                "name": f"{first} {last}",
                "position": position,
                "age": age,
                "birth_date": birth_date,
                "sweater": p.get("sweaterNumber", ""),
            })

    # Sort by last name
    players.sort(key=lambda x: x["name"].split()[-1] if " " in x["name"] else x["name"])
    return players


def fetch_all_rosters(callback=None):
    """
    Fetch rosters for all NHL teams.

    Returns a dict mapping team name -> list of player dicts.
    If callback is provided, it is called with (team_name, players) for each team loaded,
    and finally with (None, all_rosters) when complete.
    """
    all_rosters = {}
    season = _get_current_season()

    for team_name, info in NHL_TEAMS.items():
        abbr = info["abbr"]
        players = fetch_team_roster(abbr, season)
        all_rosters[team_name] = players
        if callback:
            callback(team_name, players)

    if callback:
        callback(None, all_rosters)

    return all_rosters


def fetch_all_rosters_async(callback):
    """Fetch all rosters in a background thread. Calls callback on completion."""
    thread = threading.Thread(target=fetch_all_rosters, args=(callback,), daemon=True)
    thread.start()
    return thread


def search_players(rosters, query, team_filter=None, limit=15):
    """
    Search for players across all rosters.

    Args:
        rosters: dict of team_name -> list of player dicts
        query: search string (partial name match)
        team_filter: optional team name to restrict search to
        limit: max number of results

    Returns list of (team_name, player_dict) tuples.
    """
    if not query or not rosters:
        return []

    query_lower = query.lower().strip()
    results = []

    teams_to_search = {team_filter: rosters[team_filter]} if team_filter and team_filter in rosters else rosters

    for team_name, players in teams_to_search.items():
        for player in players:
            if query_lower in player["name"].lower():
                results.append((team_name, player))
                if len(results) >= limit:
                    return results

    # Sort by best match (starts with > contains)
    results.sort(key=lambda x: (
        0 if x[1]["name"].lower().startswith(query_lower) else
        1 if any(part.lower().startswith(query_lower) for part in x[1]["name"].split()) else 2,
        x[1]["name"]
    ))

    return results[:limit]
