import requests
import base64
import json
from SpotifyAPI import (
    get_access_token,
    fetch_track_info,
    fetch_artist_info,
    fetch_album_info,
    search_spotify,
    get_recommendations,
    get_album_tracks,
    get_related_artists,
)

# Spotify API credentials
client_id = "5ec05cefccd647058cffeac2d91dc387"
client_secret = "65e2c4321945442ba9eed181ee529548"


def recommend_tracks(access_token, track_id, limit=10):
    recommendations = get_recommendations(access_token, [track_id], limit)
    if not recommendations:
        print("Failed to fetch recommendations.")
        return []

    cleaned_recommendations = clean_track_data(recommendations["tracks"])

    return cleaned_recommendations


def recommend_artists(access_token, artist_id, limit=10):
    related_artists = get_related_artists(access_token, artist_id, limit)
    if not related_artists:
        print("Failed to fetch related artists.")
        return []

    cleaned_artists = clean_artist_data(related_artists)
    return cleaned_artists


# def recommend_album_tracks(access_token, album_id, limit=10):
#     album_info = fetch_album_info(access_token, album_id)
#     if not album_info:
#         print("Failed to fetch album info.")
#         return []

#     album_name = album_info["name"]
#     album_tracks = get_album_tracks(access_token, album_id, limit)
#     if not album_tracks:
#         print("Failed to fetch album tracks.")
#         return []

#     cleaned_tracks = clean_track_data(album_tracks, album_name)
#     return cleaned_tracks


# Clean the format to display it nicely
def clean_track_data(tracks, album_name=None):
    cleaned_tracks = []
    for track in tracks:
        cleaned_track = {
            "name": track["name"],
            "id": track["id"],
            "artists": [artist["name"] for artist in track["artists"]],
            "album": album_name if album_name else track.get("album", {}).get("name"),
        }
        cleaned_tracks.append(cleaned_track)
    return cleaned_tracks


def clean_artist_data(artists):
    cleaned_artists = []
    for artist in artists:
        cleaned_artist = {
            "name": artist["name"],
            "id": artist["id"],
            "genres": artist["genres"],
            "popularity": artist["popularity"],
        }
        cleaned_artists.append(cleaned_artist)
    return cleaned_artists


def main():
    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        print("Failed to obtain access token.")
        return

    query = input("Enter the name of the track, artist, or album: ")
    search_type = input("Enter the type (track, artist, album): ").lower()

    search_results = search_spotify(access_token, query, search_type)

    # Get recommend Track, Artist or Album from the input
    if (
        search_type == "track"
        and "tracks" in search_results
        and "items" in search_results["tracks"]
        and search_results["tracks"]["items"]
    ):
        track_id = search_results["tracks"]["items"][0]["id"]
        recommendations = recommend_tracks(
            access_token,
            track_id,
        )
        print("Recommended Tracks:", json.dumps(recommendations, indent=4))

    elif (
        search_type == "artist"
        and "artists" in search_results
        and "items" in search_results["artists"]
        and search_results["artists"]["items"]
    ):
        artist_id = search_results["artists"]["items"][0]["id"]
        recommendations = recommend_artists(access_token, artist_id)
        print("Related Artists:", json.dumps(recommendations, indent=4))

    # elif (
    #     search_type == "album"
    #     and "albums" in search_results
    #     and "items" in search_results["albums"]
    #     and search_results["albums"]["items"]
    # ):
    #     album_id = search_results["albums"]["items"][0]["id"]
    #     recommendations = recommend_album_tracks(access_token, album_id)
    #     print("Album Tracks:", json.dumps(recommendations, indent=4))

    else:
        print("No results found.")


if __name__ == "__main__":
    main()
