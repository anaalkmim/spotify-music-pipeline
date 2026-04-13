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

    # --- Chart 1: Number of tracks per artist ---
    tracks_per_artist = df["artist_name"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(tracks_per_artist.index, tracks_per_artist.values, color="#1DB954")
    ax.set_xlabel("Number of Tracks")
    ax.set_title("Tracks Collected per Artist")
    plt.tight_layout()
    fig.savefig(os.path.join(PROCESSED_DIR, "tracks_per_artist.png"), dpi=150)
    plt.close()
    print("Saved: tracks_per_artist.png")

    # --- Chart 2: Average track duration by artist ---
    avg_duration = (
        df.groupby("artist_name")["duration_sec"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(avg_duration.index, avg_duration.values / 60, color="#1DB954")
    ax.set_ylabel("Average Duration (minutes)")
    ax.set_title("Average Track Duration by Artist")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(os.path.join(PROCESSED_DIR, "duration_by_artist.png"), dpi=150)
    plt.close()
    print("Saved: duration_by_artist.png")

    # --- Chart 3: Tracks by release year ---
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

    # --- Chart 4: Explicit vs Clean tracks ---
    explicit_counts = df["explicit"].value_counts()
    labels = ["Clean", "Explicit"]
    values = [explicit_counts.get(False, 0), explicit_counts.get(True, 0)]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct="%1.0f%%", colors=["#1DB954", "#b91d47"])
    ax.set_title("Explicit vs Clean Tracks")
    plt.tight_layout()
    fig.savefig(os.path.join(PROCESSED_DIR, "explicit_ratio.png"), dpi=150)
    plt.close()
    print("Saved: explicit_ratio.png")

    # --- Summary ---
    print("\n--- Summary ---")
    print(f"Total tracks: {len(df)}")
    print(f"Artists: {df['artist_name'].nunique()}")
    print(f"Longest avg duration: {avg_duration.index[0]} ({avg_duration.values[0]/60:.1f} min)")
    print(f"Explicit tracks: {values[1]} ({values[1]/len(df)*100:.0f}%)")


if __name__ == "__main__":
    analyze()
