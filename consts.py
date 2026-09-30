from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).resolve().parent

CREDS_FILE = PROJECT_DIRECTORY / "steam-search-adminkey.json"
COLLECTION_NAME = "steam_games"

RESULT_LIMIT = 100
APP_TITLE = "Steam Game Search"