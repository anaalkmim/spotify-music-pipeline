"""
Step 3: Analyze and visualize the processed data.

Generates summary statistics and charts from the clean dataset.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

PROCESSED_DIR = "data/processed"
CSV_PATH = os.path.join(PROCESSED_DIR, "tracks_clean.csv")


def analyze():
    """Generate analysis and visualizations from processed data."""
    df = pd.read_csv(CSV_PATH)

    # --- Chart 1: Top 10 most popular tracks ---
    top_tracks = df.nlargest(10, "popularity")[["track_name", "artist_name", "popularity"]]
    top_tracks["label"] = top_tracks["track_name"] + " — " + top_tracks["artist_name"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_tracks["label"], top_tracks["popularity"], color="#1DB954")
    ax.set_xlabel("Popularity")
    ax.set_title("Top 10 Most Popular Tracks")
    ax.invert_yaxis()
    plt.tight_layout()
    fig.savefig(os.path.join(PROCESSED_DIR, "top_tracks.png"), dpi=150)
    plt.close()
    print("Saved: top_tracks.png")

    # --- Chart 2: Average popularity by artist ---
    pop_by_artist = (
        df.groupby("artist_name")["popularity"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    pop_by_artist.plot(kind="bar", ax=ax, color="#1DB954")
    ax.set_ylabel("Average Popularity")
    ax.set_title("Average Track Popularity by Artist")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(PROCESSED_DIR, "popularity_by_artist.png"), dpi=150)
    plt.close()
    print("Saved: popularity_by_artist.png")

    # --- Chart 3: Tracks per year ---
    tracks_per_year = df["release_year"].dropna().astype(int).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    tracks_per_year.plot(kind="bar", ax=ax, color="#1DB954")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Tracks")
    ax.set_title("Tracks by Release Year")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(PROCESSED_DIR, "tracks_per_year.png"), dpi=150)
    plt.close()
    print("Saved: tracks_per_year.png")

    # --- Summary ---
    print("\n--- Summary ---")
    print(f"Total tracks: {len(df)}")
    print(f"Most popular track: {df.loc[df['popularity'].idxmax(), 'track_name']}")
    print(f"Most popular artist (avg): {pop_by_artist.index[0]}")


if __name__ == "__main__":
    analyze()
