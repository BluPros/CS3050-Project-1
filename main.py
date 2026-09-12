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
    r"..\games.csv",
    index_col=False
)

columns_to_keep = [
    "AppID",
    "Name",
    "Release date",
    "Price",
    "User score",
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
    "User score": "user_score",
    "Categories": "categories",
    "Genres": "genres",
    "Tags": "tags"
})

# Remove fully duplicate records
df = df.drop_duplicates(subset="app_id", keep="first")

# Remove rows missing a game name
df["name"] = df["name"].astype("string").str.strip()
df = df.dropna(subset=["name"])
df = df[df["name"] != ""]

# Remove rows with no user score
df = df[df["user_score"].notna()]

# Optional: make user_score numeric afterward
df["user_score"] = pd.to_numeric(
    df["user_score"],
    errors="coerce"
)

df.to_csv("steam_games_cleaned.csv", index=False)

print(df["user_score"].head(20))
print(df["user_score"].value_counts(dropna=False).head(20))
print(df["user_score"].dtype)