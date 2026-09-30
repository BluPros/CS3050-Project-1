# admin.py
import json
import sys
from pathlib import Path

from connector import FirebaseConnector


def load_games(json_filename):
    """Read the project JSON file and ensure it contains a list."""
    json_path = Path(json_filename)

    if not json_path.exists():
        raise FileNotFoundError(f"Data file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as file:
        games = json.load(file)

    if not isinstance(games, list):
        raise ValueError("The JSON root must be a list of game documents.")

    return games


def main():
    if len(sys.argv) != 2:
        print("Usage: python admin.py steam_games.json")
        return

    games = load_games(sys.argv[1])
    connector = FirebaseConnector()

    print("Deleting existing Steam game documents...")
    connector.delete_all_games()

    print(f"Uploading {len(games)} game documents...")
    for game in games:
        connector.upload_game(game)

    print("Upload complete.")


if __name__ == "__main__":
    main()