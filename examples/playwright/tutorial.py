from playwright.sync_api import sync_playwright
from rich import print

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://whatsmyuseragent.org/")
    print(page.title())
    browser.close()
