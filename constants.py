from dotenv import dotenv_values
import os
import urllib.parse
from pathlib import Path
from typer import get_app_dir
from enum import Enum

APP_NAME = "spotify-git-scraper"
APP_DIR: Path = Path(get_app_dir(APP_NAME))

AUTH_FILE = APP_DIR.joinpath("auth.json")
TOKEN_FILE = APP_DIR.joinpath("token_info.json")
config = {**dotenv_values(), **os.environ}

CLIENT_ID = config["SPOTIFY_CLIENT_ID"]
REDIRECT_URI = config["REDIRECT_URI"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]
SCOPE = "user-read-recently-played user-top-read user-library-read playlist-read-collaborative playlist-read-private user-follow-read"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

AUTH_STRING = config["SPOTIFY_AUTH_STRING"]


access_code_params = {
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "response_type": "code",
}

AUTH_CODE_URL = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(access_code_params)}"


class GetTopItems(str, Enum):
    artists = "artists"
    tracks = "tracks"


class GetTopTimeRanges(str, Enum):
    long_term = "long_term"
    medium_term = "medium_term"
    short_term = "short_term"
