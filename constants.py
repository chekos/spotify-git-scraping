from dotenv import dotenv_values
import os
import base64
import urllib.parse
from pathlib import Path

PARENT_FOLDER = Path(__file__).parent
AUTH_FILE = PARENT_FOLDER.joinpath("auth.json")
TOKEN_FILE = PARENT_FOLDER.joinpath("token_info.json")
config = {**dotenv_values(), **os.environ}

CLIENT_ID = config["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = config["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = config["REDIRECT_URI"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]
SCOPE = "user-read-recently-played user-top-read user-library-read playlist-read-collaborative"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

AUTH_STRING = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")).decode(
    "utf-8"
)


access_code_params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "response_type": "code",
}

AUTH_CODE_URL = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(access_code_params)}"
