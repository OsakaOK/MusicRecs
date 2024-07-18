import requests
import base64
from pymongo import MongoClient

# Spotify API credentials
client_id = "your client id"
client_secret = "your client secret"

# MongoDB Configuration
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["music_recommendation"]
tracks_collection = db["tracks"]
artists_collection = db["artists"]
recommendations_collection = db["recommendations"]


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


# # Fetching data to display
# def fetch_track_info(access_token, track_id):
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#     }
#     response = requests.get(
#         f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers
#     )
#     return response.json() if response.status_code == 200 else None


# def fetch_artist_info(access_token, artist_id):
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#     }
#     response = requests.get(
#         f"https://api.spotify.com/v1/artists/{artist_id}", headers=headers
#     )
#     return response.json() if response.status_code == 200 else None


# def fetch_album_info(access_token, album_id):
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#     }
#     response = requests.get(
#         f"https://api.spotify.com/v1/albums/{album_id}", headers=headers
#     )
#     return response.json() if response.status_code == 200 else None


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


def recommend_tracks(access_token, track_id, limit=10):
    recommendations = get_recommendations(access_token, [track_id], limit)
    if not recommendations:
        print("Failed to fetch recommendations.")
        return []

    cleaned_recommendations = clean_track_data(recommendations["tracks"])

    return cleaned_recommendations


def recommend_artists(access_token, artist_ids, limit=10):
    all_related_artists = []
    for artist_id in artist_ids:
        related_artists = get_related_artists(access_token, artist_id, limit)
        if related_artists:
            all_related_artists.extend(related_artists)

    cleaned_artists = clean_artist_data(all_related_artists[:limit])
    return cleaned_artists


# Clean the format to display it nicely
def clean_track_data(tracks, album_name=None):
    seen_ids = set()
    cleaned_tracks = []
    for track in tracks:
        if track["id"] not in seen_ids:
            seen_ids.add(track["id"])
            cleaned_track = {
                "name": track["name"],
                "id": track["id"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album": track.get("album", {}).get("name", "Unknown Album"),
            }
            cleaned_tracks.append(cleaned_track)
    return cleaned_tracks


def clean_artist_data(artists):
    seen_ids = set()
    cleaned_artists = []
    for artist in artists:
        if artist["id"] not in seen_ids:
            seen_ids.add(artist["id"])
            cleaned_artist = {
                "name": artist["name"],
                "id": artist["id"],
                "genres": artist.get("genres", []),
                "popularity": artist.get("popularity", 0),
            }
            cleaned_artists.append(cleaned_artist)
    return cleaned_artists


def cache_search_results(search_type, query, results):
    collection = tracks_collection if search_type == "track" else artists_collection
    collection.update_one({"query": query}, {"$set": {"results": results}}, upsert=True)


def get_cached_search_results(search_type, query):
    collection = tracks_collection if search_type == "track" else artists_collection
    cached_result = collection.find_one({"query": query})
    if cached_result:
        return cached_result["results"]
    return None


def cache_recommendations(track_id, recommendations):
    recommendations_collection.update_one(
        {"track_id": track_id},
        {"$set": {"recommendations": recommendations}},
        upsert=True,
    )


def get_cached_recommendations(track_id):
    cached_result = recommendations_collection.find_one({"track_id": track_id})
    if cached_result:
        return cached_result["recommendations"]
    return None
