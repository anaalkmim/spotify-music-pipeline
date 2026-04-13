"""
Spotify Music Pipeline — Main runner.

Executes the full ETL pipeline:
  1. Extract: Fetch data from Spotify API
  2. Transform: Clean and structure the data
  3. Analyze: Generate stats and visualizations

Usage:
    python main.py
"""

from src.extract import extract
from src.transform import transform
from src.analyze import analyze


def run_pipeline():
    """Run the full pipeline."""
    print("=" * 50)
    print("STEP 1: Extracting data from Spotify API")
    print("=" * 50)
    extract()

    print()
    print("=" * 50)
    print("STEP 2: Transforming raw data")
    print("=" * 50)
    transform()

    print()
    print("=" * 50)
    print("STEP 3: Analyzing and visualizing")
    print("=" * 50)
    analyze()

    print()
    print("Pipeline complete!")


if __name__ == "__main__":
    run_pipeline()
