import base64
import time

from rich import print
from dotenv import dotenv_values
import httpx

config = dotenv_values()


def _is_token_expired(expires_at):
    now = int(time.time())
    return expires_at - now < 60


def get_token():
    auth_string = base64.b64encode(
        f"{config['SPOTIFY_CLIENT_ID']}:{config['SPOTIFY_CLIENT_SECRET']}".encode(
            "utf-8"
        )
    ).decode("ascii")

    headers = {
        "Authorization": f"Basic {auth_string}",
    }

    response = httpx.post(
        url="https://accounts.spotify.com/api/token",
        headers=headers,
        data={"grant_type": "client_credentials"},
        verify=True,
    )
    response_data = response.json()
    response_data["expires_at"] = int(response_data["expires_in"]) + int(time.time())

    return response_data


token_info = get_token()
if _is_token_expired(token_info["expires_at"]):
    token_info = get_token()

token = token_info["access_token"]

def get_recently_played(token, time, before_or_after, limit):
    url = "https://api.spotify.com/v1/me/player/recently-played"

    header = {"Authorization": token, "content-type": "application/json"}

    params = {before_or_after: time, "limit": limit}

    response = httpx.get(url, headers=header, params=params)

    return response.json()

data = get_recently_played(token, int(time.time()), 'before', 10)

