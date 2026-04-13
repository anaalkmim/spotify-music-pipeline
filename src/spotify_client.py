"""
Spotify API client module.
Handles authentication and data fetching from the Spotify Web API.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1"


def get_access_token():
    """Authenticate with Spotify using Client Credentials flow."""
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET),
    )
    response.raise_for_status()
    return response.json()["access_token"]


def search_artist(token, artist_name):
    """Search for an artist by name and return the first match."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}

    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    response.raise_for_status()

    items = response.json()["artists"]["items"]
    if not items:
        return None
    return items[0]


def search_tracks(token, artist_name, limit=10):
    """Search for tracks by an artist using the search endpoint."""
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": f"artist:{artist_name}",
        "type": "track",
        "limit": limit,
    }

    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    response.raise_for_status()
    return response.json()["tracks"]["items"]
