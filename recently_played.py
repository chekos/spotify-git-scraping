from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import requests
import urllib.parse
import os
import time
import sqlalchemy
import pandas as pd
import datetime as dt
import sqlite3


opts = Options()

opts.set_headless()

assert opts.headless  # Operating in headless mode

browser = Firefox(options=opts)
browser.get("https://duckduckgo.com")

CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
USERNAME = os.environ.get("SPOTIFY_USERNAME")
PASSWORD = os.environ.get("SPOTIFY_PASSWORD")

SCOPE = "user-read-recently-played"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"

access_code_params = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "response_type": "code",
}


browser.get(f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(access_code_params)}")

username = browser.find_element_by_id("login-username")
username.send_keys(USERNAME)

password = browser.find_element_by_id("login-password")
password.send_keys(PASSWORD)

login_button = browser.find_element_by_id("login-button")
login_button.click()
time.sleep(4)

# TODO add test
ACCESS_TOKEN = browser.current_url.split("code=")[-1]

TOKEN_API_URL = "https://accounts.spotify.com/api/token"
response = requests.post(
    TOKEN_API_URL,
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": ACCESS_TOKEN,
    },
)

# TODO add test
r_dicts = response.json()


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
# TOKEN = "" # your Spotify API token

# Generate your token here:  https://developer.spotify.com/console/get-recently-played/
# Note: You need a Spotify account (can be easily created for free)


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    # Primary Key Check
    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Check that all timestamps are of yesterday's date
    #     an_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    # #     yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    #     timestamps = df["timestamp"].tolist()
    #     for timestamp in timestamps:
    #         if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
    #             raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True


TOKEN = r_dicts["access_token"]

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

# Convert time to Unix timestamp in miliseconds
today = dt.datetime.now()
an_hour_ago = today - dt.timedelta(hours=1)
an_hour_ago_unix_timestamp = int(an_hour_ago.timestamp()) * 1000

# Download all songs you've listened to in the last hour
API_REQUEST = f"https://api.spotify.com/v1/me/player/recently-played?after={an_hour_ago_unix_timestamp}"
r = requests.get(API_REQUEST, headers=headers)

data = r.json()

song_names = []
artist_names = []
played_at_list = []
timestamps = []

# Extracting only the relevant bits of data from the json object
for song in data["items"]:
    song_names.append(song["track"]["name"])
    artist_names.append(song["track"]["album"]["artists"][0]["name"])
    played_at_list.append(song["played_at"])
    timestamps.append(song["played_at"][0:10])

# Prepare a dictionary in order to turn it into a pandas dataframe below
song_dict = {
    "song_name": song_names,
    "artist_name": artist_names,
    "played_at": played_at_list,
    "timestamp": timestamps,
}

song_df = pd.DataFrame(
    song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"]
)

# Validate
if check_if_valid_data(song_df):
    print("Data valid, proceed to Load stage")

# Load
engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = sqlite3.connect("my_played_tracks.sqlite")
cursor = conn.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS my_played_tracks(
    song_name VARCHAR(200),
    artist_name VARCHAR(200),
    played_at VARCHAR(200),
    timestamp VARCHAR(200),
    CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
)
"""

cursor.execute(sql_query)
print("Opened database successfully")

try:
    song_df.to_sql("my_played_tracks", engine, index=False, if_exists="append")
except:
    print("Data already exists in the database")

conn.close()
print("Close database successfully")