from constants import (
    AUTH_CODE_URL,
    REDIRECT_URI,
    USERNAME,
    PASSWORD,
)

from playwright.sync_api import sync_playwright


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
        page.wait_for_url(f"{REDIRECT_URI}**")

        # Authorized page
        auth = {}
        auth["code"] = page.url.split("code=")[-1]
        if write:
            import json

            with open("auth.json", "w") as auth_file:
                json.dump(auth, auth_file)

        return auth


if __name__ == "__main__":
    retrieve_code(write=True)
