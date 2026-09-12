# AppID, Name, Release date, Estimated owners, Peak CCU, Required age, Price
# DiscountDLC count, About the game, Supported languages, Full audio languages
# Reviews, Header image, Website, Support url, Support email, Windows, Mac, Linux
# Metacritic score, Metacritic url, User score, Positive, Negative, Score rank 
# Achievements, Recommendations, Notes, Average playtime forever
# Average playtime two weeks, Median playtime forever, Median playtime two weeks
# Developers, Publishers, Categories, Genres, Tags, Screenshots, Movies

import pandas as pd
import sqlite3

# index_col=False prevents pandas from treating AppID as an index
df = pd.read_csv(
    "C:\\Users\\blupr\\Downloads\\CS3050\\CS3050-Project-1\\games.csv",
    index_col=False
)

columns_to_keep = [
    "AppID",
    "Name",
    "Release date",
    "Price",
    "Metacritic url",
    "Categories",
    "Genres",
    "Tags"
]

df = df[columns_to_keep]

df = df.rename(columns={
    "AppID": "app_id",
    "Name": "name",
    "Release date": "release_date",
    "Price": "price",
    "Metacritic url": "metacritic_url",
    "Categories": "categories",
    "Genres": "genres",
    "Tags": "tags"
})

df = df.drop_duplicates(subset="app_id", keep="first")

df["name"] = df["name"].astype("string").str.strip()
df = df.dropna(subset=["name"])
df = df[df["name"] != ""]

df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

five_years_ago = pd.Timestamp("2021-09-12")
df = df[df["release_date"] >= five_years_ago]

df = df[df["metacritic_url"].notna()]

df.to_csv("steam_games_cleaned.csv", index=False)