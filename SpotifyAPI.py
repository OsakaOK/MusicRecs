import requests
import base64

# Spotify API credentials
client_id = "5ec05cefccd647058cffeac2d91dc387"
client_secret = "65e2c4321945442ba9eed181ee529548"


def get_access_token(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    auth_url = "https://accounts.spotify.com/api/token"
    auth_headers = {
        "Authorization": f"Basic {encoded_credentials}",
    }
    auth_data = {
        "grant_type": "client_credentials",
    }
    response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    response_data = response.json()
    return response_data.get("access_token")


def search_spotify(access_token, query, search_type):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    params = {"q": query, "type": search_type, "limit": 1}
    response = requests.get(
        "https://api.spotify.com/v1/search", headers=headers, params=params
    )
    return response.json()


def fetch_track_info(access_token, track_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers
    )
    return response.json() if response.status_code == 200 else None


def fetch_artist_info(access_token, artist_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers
    )
    return response.json() if response.status_code == 200 else None


def fetch_album_info(access_token, album_id):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}", headers=headers
    )
    return response.json() if response.status_code == 200 else None
