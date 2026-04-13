"""
Tests for the transform module.
"""

import json
import os
import pandas as pd
import pytest
from src.transform import transform

SAMPLE_DATA = [
    {
        "artist_name": "Test Artist",
        "artist_genres": ["rock", "indie"],
        "track_name": "Song A",
        "track_id": "abc123",
        "album_name": "Album X",
        "release_date": "2023-05-15",
        "popularity": 85,
        "duration_ms": 210000,
        "explicit": False,
    },
    {
        "artist_name": "Test Artist",
        "artist_genres": ["rock", "indie"],
        "track_name": "Song B",
        "track_id": "def456",
        "album_name": "Album X",
        "release_date": "2023-05-15",
        "popularity": 72,
        "duration_ms": 185000,
        "explicit": True,
    },
    {
        "artist_name": "Another Artist",
        "artist_genres": [],
        "track_name": "Song C",
        "track_id": "ghi789",
        "album_name": "Album Y",
        "release_date": "2020",
        "popularity": 60,
        "duration_ms": 300000,
        "explicit": False,
    },
    {
        "artist_name": "Another Artist",
        "artist_genres": [],
        "track_name": "Song C Duplicate",
        "track_id": "ghi789",
        "album_name": "Album Y",
        "release_date": "2020",
        "popularity": 60,
        "duration_ms": 300000,
        "explicit": False,
    },
]


@pytest.fixture
def setup_raw_data(tmp_path):
    """Create temporary raw data file for testing."""
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    raw_path = raw_dir / "tracks_raw.json"
    with open(raw_path, "w") as f:
        json.dump(SAMPLE_DATA, f)

    return tmp_path


def test_transform_removes_duplicates(setup_raw_data, monkeypatch):
    """Tracks with the same track_id should be deduplicated."""
    tmp_path = setup_raw_data
    monkeypatch.setattr("src.transform.RAW_PATH", str(tmp_path / "data" / "raw" / "tracks_raw.json"))
    monkeypatch.setattr("src.transform.PROCESSED_DIR", str(tmp_path / "data" / "processed"))

    df = transform()
    track_ids = df["track_id"].tolist()
    assert len(track_ids) == len(set(track_ids)), "Duplicate track_ids found"


def test_transform_converts_duration(setup_raw_data, monkeypatch):
    """Duration should be converted from ms to seconds."""
    tmp_path = setup_raw_data
    monkeypatch.setattr("src.transform.RAW_PATH", str(tmp_path / "data" / "raw" / "tracks_raw.json"))
    monkeypatch.setattr("src.transform.PROCESSED_DIR", str(tmp_path / "data" / "processed"))

    df = transform()
    assert "duration_sec" in df.columns, "duration_sec column missing"
    assert "duration_ms" not in df.columns, "duration_ms should be removed"
    assert df.loc[df["track_id"] == "abc123", "duration_sec"].values[0] == 210.0


def test_transform_parses_release_year(setup_raw_data, monkeypatch):
    """Release dates should be parsed and release_year extracted."""
    tmp_path = setup_raw_data
    monkeypatch.setattr("src.transform.RAW_PATH", str(tmp_path / "data" / "raw" / "tracks_raw.json"))
    monkeypatch.setattr("src.transform.PROCESSED_DIR", str(tmp_path / "data" / "processed"))

    df = transform()
    assert "release_year" in df.columns
    assert 2023.0 in df["release_year"].values
    assert 2020.0 in df["release_year"].values


def test_transform_genres_to_string(setup_raw_data, monkeypatch):
    """Genre lists should be converted to comma-separated strings."""
    tmp_path = setup_raw_data
    monkeypatch.setattr("src.transform.RAW_PATH", str(tmp_path / "data" / "raw" / "tracks_raw.json"))
    monkeypatch.setattr("src.transform.PROCESSED_DIR", str(tmp_path / "data" / "processed"))

    df = transform()
    genres = df.loc[df["track_id"] == "abc123", "artist_genres"].values[0]
    assert genres == "rock, indie"


def test_transform_sorts_by_artist_and_popularity(setup_raw_data, monkeypatch):
    """Results should be sorted by artist name asc, then popularity desc."""
    tmp_path = setup_raw_data
    monkeypatch.setattr("src.transform.RAW_PATH", str(tmp_path / "data" / "raw" / "tracks_raw.json"))
    monkeypatch.setattr("src.transform.PROCESSED_DIR", str(tmp_path / "data" / "processed"))

    df = transform()
    assert df.iloc[0]["artist_name"] == "Another Artist"
    assert df.iloc[1]["artist_name"] == "Test Artist"
    assert df.iloc[1]["popularity"] >= df.iloc[2]["popularity"]


def test_transform_saves_csv(setup_raw_data, monkeypatch):
    """CSV file should be created in the processed directory."""
    tmp_path = setup_raw_data
    monkeypatch.setattr("src.transform.RAW_PATH", str(tmp_path / "data" / "raw" / "tracks_raw.json"))
    monkeypatch.setattr("src.transform.PROCESSED_DIR", str(tmp_path / "data" / "processed"))

    transform()
    csv_path = tmp_path / "data" / "processed" / "tracks_clean.csv"
    assert csv_path.exists(), "CSV file was not created"

    df_csv = pd.read_csv(csv_path)
    assert len(df_csv) == 3
