import requests
import base64

# Spotify API credentials
client_id = "your client id"
client_secret = "your client secret"


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


def search_spotify(access_token, query, search_type, limit=10):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    params = {
        "q": query,
        "type": search_type,
        "limit": limit,  # Increase limit to get more results
    }
    response = requests.get(
        "https://api.spotify.com/v1/search", headers=headers, params=params
    )
    return response.json()


# Fetching data to display
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


# Functions to enhance the recommendation
def get_recommendations(access_token, seed_tracks, limit):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    params = {
        "seed_tracks": ",".join(seed_tracks),
        "limit": limit,  # Number of tracks you want it to recommend change above parameter
    }
    response = requests.get(
        "https://api.spotify.com/v1/recommendations", headers=headers, params=params
    )
    return response.json() if response.status_code == 200 else None


def get_related_artists(access_token, artist_id, limit):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/related-artists",
        headers=headers,
    )
    related_artists = response.json() if response.status_code == 200 else None
    if related_artists and "artists" in related_artists:
        return related_artists["artists"][:limit]
    return None
