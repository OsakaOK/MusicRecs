import requests
import base64
import json
from pymongo import MongoClient

client_id = "5ec05cefccd647058cffeac2d91dc387"
client_secret = "65e2c4321945442ba9eed181ee529548"
redirect_uri = "your_redirect_uri"


# Function to get access token
def get_access_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(
        (client_id + ":" + client_secret).encode("ascii")
    ).decode("ascii")
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(
        auth_url, headers={"Authorization": "Basic " + auth_header}, data=auth_data
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Failed to get access token")
        return None


# Function to search Spotify
def search_spotify(access_token, query, search_type, limit=10):
    search_url = (
        f"https://api.spotify.com/v1/search?q={query}&type={search_type}&limit={limit}"
    )
    response = requests.get(
        search_url, headers={"Authorization": "Bearer " + access_token}
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to search Spotify")
        return None


# Function to get track recommendations
def get_recommendations(access_token, track_ids, limit=10):
    rec_url = f"https://api.spotify.com/v1/recommendations?seed_tracks={','.join(track_ids)}&limit={limit}"
    response = requests.get(
        rec_url, headers={"Authorization": "Bearer " + access_token}
    )

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get recommendations")
        return None


# Function to get related artists
def get_related_artists(access_token, artist_id, limit=10):
    related_url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    response = requests.get(
        related_url, headers={"Authorization": "Bearer " + access_token}
    )

    if response.status_code == 200:
        return response.json()["artists"][:limit]
    else:
        print("Failed to get related artists")
        return None


# Function to clean track data
def clean_track_data(tracks):
    cleaned_tracks = []
    for track in tracks:
        track_info = {
            "id": track["id"],
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
        }
        cleaned_tracks.append(track_info)
    return cleaned_tracks


# Function to clean artist data
def clean_artist_data(artists):
    cleaned_artists = []
    for artist in artists:
        artist_info = {
            "id": artist["id"],
            "name": artist["name"],
            "genres": artist["genres"],
            "popularity": artist["popularity"],
            "followers": artist["followers"]["total"],
        }
        cleaned_artists.append(artist_info)
    return cleaned_artists


# Connect to MongoDB
def connect_to_mongo():
    client = MongoClient("localhost", 27017)
    db = client["music_recommendation"]
    return db


# Cache search results
def cache_search_results(db, search_type, query, limit, results):
    collection = db[search_type + "_search"]
    collection.insert_one({"query": query, "limit": limit, "results": results})


# Get cached search results
def get_cached_search_results(db, search_type, query, limit):
    collection = db[search_type + "_search"]
    cached = collection.find_one({"query": query, "limit": limit})
    return cached["results"] if cached else None


# Cache recommendations
def cache_recommendations(db, item_id, recommendations):
    collection = db["recommendations"]
    collection.insert_one({"item_id": item_id, "recommendations": recommendations})


# Get cached recommendations
def get_cached_recommendations(db, item_id):
    collection = db["recommendations"]
    cached = collection.find_one({"item_id": item_id})
    return cached["recommendations"] if cached else None
