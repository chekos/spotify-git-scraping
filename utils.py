import json
from datetime import datetime as dt, timedelta

from constants import (
    AUTH_FILE,
    SCOPE,
    TOKEN_FILE,
    AUTH_STRING,
    AUTH_CODE_URL,
    REDIRECT_URI,
    SPOTIFY_TOKEN_URL,
    USERNAME,
    PASSWORD,
)

import httpx
from playwright.sync_api import sync_playwright


def is_expired(expires_at):
    now = dt.now()
    return now > dt.fromisoformat(expires_at)


def retrieve_code(write: bool = False):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(AUTH_CODE_URL)

        # Interact with login form
        page.locator("#login-username").fill(USERNAME)
        page.locator("#login-password").fill(PASSWORD)
        page.locator("#login-button").click()
        try:
            page.locator("[data-testid=auth-accept]").click(timeout=3_000)
        except:
            pass
        page.wait_for_url(f"{REDIRECT_URI}**")

        # Authorized page
        auth = {}
        auth["code"] = page.url.split("code=")[-1]
        auth["scope"] = SCOPE

        if write:

            with open(AUTH_FILE, "w") as auth_file:
                json.dump(auth, auth_file)

        return auth


def request_token(
    code: str,
    write: bool = False,
):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Authorization": f"Basic {AUTH_STRING}"}

    response = httpx.post(
        url=SPOTIFY_TOKEN_URL, headers=headers, data=data, verify=True
    )
    response_data = response.json()

    response_data["expires_at"] = dt.now() + timedelta(
        seconds=int(response_data["expires_in"])
    )

    if write:
        with open(TOKEN_FILE, "w") as token_file:
            json.dump(response_data, token_file, default=str)

    return response_data


def refresh_token(
    refresh_token: str,
    write: bool = False,
):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {"Authorization": f"Basic {AUTH_STRING}"}

    response = httpx.post(
        url=SPOTIFY_TOKEN_URL, headers=headers, data=data, verify=True
    )
    response_data = response.json()

    response_data["expires_at"] = dt.now() + timedelta(
        seconds=int(response_data["expires_in"])
    )

    if write:
        with open(TOKEN_FILE, "w") as token_file:
            json.dump(response_data, token_file, default=str)

    return response_data


def handle_authorization(save_files: bool = False):
    if AUTH_FILE.exists():
        with open(AUTH_FILE, "r") as auth_file:
            auth = json.load(auth_file)

        if auth["scope"] != SCOPE:
            # need new code
            auth = retrieve_code(write=save_files)
    else:
        auth = retrieve_code(write=save_files)

    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "r") as token_file:
            token_info = json.load(token_file)

        if is_expired(token_info["expires_at"]):
            token_info = refresh_token(token_info["refresh_token"], write=save_files)
    else:
        token_info = request_token(auth["code"], write=save_files)

    return token_info


if __name__ == "__main__":
    handle_authorization(save_files=True)
