"""
Step 1: Extract raw data from Spotify API.

Fetches track data for a list of artists using the search endpoint,
then saves the raw JSON responses to data/raw/.
"""

import json
import os
from src.spotify_client import get_access_token, search_artist, search_tracks

ARTISTS = [
    "Nothing But Thieves",
    "Pink Floyd",
    "Foo Fighters",
    "Adele",
    "Billie Eilish",
    "Ren",
    "Lady Gaga",
    "The Black Keys",
    "Slipknot",
    "Twenty One Pilots",
]

RAW_DIR = "data/raw"


def extract():
    """Fetch data from Spotify API and save raw JSON files."""
    os.makedirs(RAW_DIR, exist_ok=True)

    token = get_access_token()
    all_tracks = []

    for artist_name in ARTISTS:
        print(f"Fetching data for: {artist_name}")

        artist = search_artist(token, artist_name)
        if artist is None:
            print(f"  Artist not found: {artist_name}, skipping.")
            continue

        tracks = search_tracks(token, artist_name, limit=10)

        for track in tracks:
            all_tracks.append(
                {
                    "artist_name": artist["name"],
                    "artist_genres": artist.get("genres", []),
                    "track_name": track["name"],
                    "track_id": track["id"],
                    "album_name": track["album"]["name"],
                    "release_date": track["album"].get("release_date", ""),
                    "popularity": track.get("popularity", 0),
                    "duration_ms": track.get("duration_ms", 0),
                    "explicit": track.get("explicit", False),
                }
            )

    output_path = os.path.join(RAW_DIR, "tracks_raw.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_tracks, f, ensure_ascii=False, indent=2)

    print(f"\nExtracted {len(all_tracks)} tracks from {len(ARTISTS)} artists.")
    print(f"Raw data saved to {output_path}")


if __name__ == "__main__":
    extract()
