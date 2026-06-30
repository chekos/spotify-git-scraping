# `#git-scraping` my spotify data

## Status

This repo is retired as the scheduled raw Spotify fetcher. It is kept as a
historical source-data repo for the Spotify/git-scraping migration.

Current canonical listening data now lives in
[`chekos/my-spotify-data`](https://github.com/chekos/my-spotify-data). Current
analytics and GitHub Pages output live in
[`chekos/my-spotify-analytics`](https://github.com/chekos/my-spotify-analytics).

`my-spotify-data` still reads this repo's full Git history when rebuilding the
no-data-loss canonical audit, so do not archive or delete this repo while that
dependency remains.

GitHub Actions in this repo are retained only for recovery reference and should
remain disabled unless there is an intentional historical rebuild.

## Original checklist

- [x] Step 1: Authenticate user (retrieve access token)
- [x] Step 2: Use that access token to access endpoints of interest
- [x] Step 3: Save data

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
