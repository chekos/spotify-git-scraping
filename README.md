# `#git-scraping` my spotify data

- [x] Step 1: Authenticate user (retrieve access token)
- [x] Step 2: Use that access token to access endpoints of interest
Step 3: Save data

## Reference
* Retrieving Access Token: [docs](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/)
* Playwright docs: https://playwright.dev/python/docs/library 
* Playwright | Authentication state: https://playwright.dev/python/docs/auth

## Playwright steps
* Installation and only get chromium (instead of all three browsers)
```shell
python3 -m pip install playwright
playwright install chromium
```