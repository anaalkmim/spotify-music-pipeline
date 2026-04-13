# Spotify Music Pipeline

A Python data pipeline that extracts music data from the Spotify Web API, transforms it into a clean dataset, and generates analysis with visualizations.

## What it does

1. **Extract** — Fetches top tracks and audio features (danceability, energy, valence, tempo, etc.) for a configurable list of artists via the Spotify API.
2. **Transform** — Cleans the raw data: parses dates, removes duplicates, handles missing values, converts units, and saves as CSV and Parquet.
3. **Analyze** — Generates summary statistics and charts: top tracks by popularity, danceability comparison across artists, and energy vs. valence scatter plots.

## Project structure

```
spotify-music-pipeline/
├── main.py                  # Runs the full pipeline
├── src/
│   ├── spotify_client.py    # Spotify API authentication and requests
│   ├── extract.py           # Step 1: data extraction
│   ├── transform.py         # Step 2: data cleaning and transformation
│   └── analyze.py           # Step 3: analysis and visualizations
├── data/
│   ├── raw/                 # Raw JSON from API (git-ignored)
│   └── processed/           # Clean CSV/Parquet + charts (git-ignored)
├── requirements.txt
├── .env.example             # Template for API credentials
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/spotify-music-pipeline.git
cd spotify-music-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Spotify credentials

Create a Spotify Developer account at [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and create an app to get your Client ID and Client Secret.

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 5. Run the pipeline

```bash
python main.py
```

## Customization

Edit the `ARTISTS` list in `src/extract.py` to collect data for any artists you want:

```python
ARTISTS = [
    "Kendrick Lamar",
    "Beyoncé",
    "Arctic Monkeys",
    # Add your favorites here
]
```

## Sample output

After running the pipeline, you'll find in `data/processed/`:

- `tracks_clean.csv` — Clean dataset with all tracks and audio features
- `tracks_clean.parquet` — Same data in Parquet format
- `top_tracks.png` — Bar chart of the 10 most popular tracks
- `danceability_by_artist.png` — Average danceability by artist
- `energy_vs_valence.png` — Scatter plot of energy vs. valence (positivity)

## Tech stack

- **Python 3.10+**
- **requests** — HTTP client for Spotify API
- **pandas** — Data manipulation and cleaning
- **matplotlib** — Data visualization
- **python-dotenv** — Environment variable management

## License

MIT
