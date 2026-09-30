# AppID, Name, Release date, Estimated owners, Peak CCU, Required age, Price
# DiscountDLC count, About the game, Supported languages, Full audio languages
# Reviews, Header image, Website, Support url, Support email, Windows, Mac, Linux
# Metacritic score, Metacritic url, User score, Positive, Negative, Score rank 
# Achievements, Recommendations, Notes, Average playtime forever
# Average playtime two weeks, Median playtime forever, Median playtime two weeks
# Developers, Publishers, Categories, Genres, Tags, Screenshots, Movies

# prepare_data.py
import json
from pathlib import Path

import pandas as pd

INPUT_CSV = Path("..\\games.csv")
OUTPUT_JSON = Path("steam_games_cleaned.json")
MIN_RELEASE_DATE = pd.Timestamp("2021-09-12")

COLUMNS_TO_KEEP = [
    "AppID",
    "Name",
    "Release date",
    "Price",
    "Metacritic url",
    "Genres",
]

RENAME_COLUMNS = {
    "AppID": "app_id",
    "Name": "name",
    "Release date": "release_date",
    "Price": "price",
    "Metacritic url": "metacritic_url",
    "Genres": "genre",
}


def clean_text(value):
    """Return a trimmed string, or None for missing/empty values."""
    if pd.isna(value):
        return None

    value = str(value).strip()
    return value if value else None


def main():
    data_frame = pd.read_csv(INPUT_CSV, index_col=False)
    data_frame = data_frame[COLUMNS_TO_KEEP].rename(columns=RENAME_COLUMNS)

    data_frame = data_frame.drop_duplicates(subset="app_id", keep="first")
    data_frame["name"] = data_frame["name"].map(clean_text)
    data_frame = data_frame.dropna(subset=["name"])

    data_frame["release_date"] = pd.to_datetime(
        data_frame["release_date"],
        errors="coerce"
    )
    data_frame = data_frame.dropna(subset=["release_date"])
    data_frame = data_frame[data_frame["release_date"] >= MIN_RELEASE_DATE]

    data_frame["price"] = pd.to_numeric(data_frame["price"], errors="coerce")
    data_frame = data_frame.dropna(subset=["price"])

    records = []

    for row in data_frame.itertuples(index=False):
        record = {
            "app_id": int(row.app_id),
            "name": row.name,
            "release_year": int(row.release_date.year),
            "price": float(row.price),
            "genre": clean_text(row.genre) or "Unknown",
            "has_metacritic": clean_text(row.metacritic_url) is not None,
        }

        metacritic_url = clean_text(row.metacritic_url)
        if metacritic_url is not None:
            record["metacritic_url"] = metacritic_url

        records.append(record)

    with OUTPUT_JSON.open("w", encoding="utf-8") as output_file:
        json.dump(records, output_file, indent=2, ensure_ascii=False)

    print(f"Wrote {len(records)} games to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()