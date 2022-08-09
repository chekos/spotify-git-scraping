from dotenv import dotenv_values

config = dotenv_values()

CLIENT_ID = config['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = config['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
SCOPE = 'user-read-recently-played'
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"