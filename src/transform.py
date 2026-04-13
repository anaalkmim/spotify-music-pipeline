"""
Step 2: Transform raw data into a clean, analysis-ready dataset.

Reads raw JSON, applies cleaning and transformations,
then saves to data/processed/ as CSV and Parquet.
"""

import json
import os
import pandas as pd

RAW_PATH = "data/raw/tracks_raw.json"
PROCESSED_DIR = "data/processed"


def transform():
    """Clean and transform raw track data."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)

    # Convert duration from milliseconds to seconds
    df["duration_sec"] = (df["duration_ms"] / 1000).round(1)
    df = df.drop(columns=["duration_ms"])

    # Parse release date to datetime
    df["release_date"] = pd.to_datetime(df["release_date"], format="mixed", errors="coerce")
    df["release_year"] = df["release_date"].dt.year

    # Convert genres list to comma-separated string
    df["artist_genres"] = df["artist_genres"].apply(
        lambda genres: ", ".join(genres) if isinstance(genres, list) else ""
    )

    # Remove duplicate tracks (same track_id)
    df = df.drop_duplicates(subset=["track_id"])

    # Sort by artist name, then track name
    df = df.sort_values(["artist_name", "track_name"])
    df = df.reset_index(drop=True)

    # Save as CSV
    csv_path = os.path.join(PROCESSED_DIR, "tracks_clean.csv")
    df.to_csv(csv_path, index=False)

    # Save as Parquet
    parquet_path = os.path.join(PROCESSED_DIR, "tracks_clean.parquet")
    df.to_parquet(parquet_path, index=False)

    print(f"Transformed {len(df)} tracks.")
    print(f"Saved to {csv_path} and {parquet_path}")

    print(f"\nArtists: {df['artist_name'].nunique()}")
    print(f"Tracks: {len(df)}")
    if df["release_year"].notna().any():
        print(f"Year range: {int(df['release_year'].min())} - {int(df['release_year'].max())}")

    return df


if __name__ == "__main__":
    transform()
