import json
import requests
from dotenv import load_dotenv
from utils.config import get_secret
from utils.styling import apply_custom_style
apply_custom_style()

load_dotenv()

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-host": get_secret("RAPIDAPI_HOST"),
    "x-rapidapi-key": get_secret("RAPIDAPI_KEY")
}

def _get(endpoint, params=None):
    """Internal helper: makes a GET request and handles errors cleanly."""
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Request to {endpoint} timed out")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {endpoint}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {endpoint}: {e}")
        return None

def get_live_matches():
    return _get("matches/v1/live")

def get_recent_matches():
    return _get("matches/v1/recent")

def get_upcoming_matches():
    return _get("matches/v1/upcoming")

def get_scorecard(match_id):
    return _get(f"mcenter/v1/{match_id}/scard")

def get_top_stats(stats_type="mostRuns"):
    return _get("stats/v1/topstats/0", params={"statsType": stats_type})

#if __name__ == "__main__":
#    data = get_live_matches()
#    if data:
#        print("Live matches fetched successfully")
#        print(data)
#    else:
#        print("Failed to fetch live matches")