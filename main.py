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

    query = input("Enter the name of the track or artist: ")
    search_type = input("Enter the type (track or artist): ").lower()
    search_limit = int(input("Enter the number of search results to display: "))
    limit = int(input("Enter the number of recommendations: "))

    search_results = search_spotify(
        access_token, query, search_type, limit=search_limit
    )

    # Get recommend Track or Artist from the input
    if (
        search_type == "track"
        and "tracks" in search_results
        and "items" in search_results["tracks"]
        and search_results["tracks"]["items"]
    ):
        print("Search Results:")
        for idx, track in enumerate(search_results["tracks"]["items"]):
            track_name = track["name"]
            artist_names = ", ".join([artist["name"] for artist in track["artists"]])
            print(f"{idx + 1}: {track_name} by {artist_names}")

        track_selection = (
            int(input("Enter the number of the track you want recommendations for: "))
            - 1
        )
        if 0 <= track_selection < len(search_results["tracks"]["items"]):
            track_id = search_results["tracks"]["items"][track_selection]["id"]
            recommendations = recommend_tracks(access_token, track_id, limit)
            print("Recommended Tracks:", json.dumps(recommendations, indent=4))
        else:
            print("Invalid selection.")

    elif (
        search_type == "artist"
        and "artists" in search_results
        and "items" in search_results["artists"]
        and search_results["artists"]["items"]
    ):
        print("Search Results:")
        for idx, artist in enumerate(search_results["artists"]["items"]):
            artist_name = artist["name"]
            print(f"{idx + 1}: {artist_name}")

        artist_selection = (
            int(input("Enter the number of the artist you want recommendations for: "))
            - 1
        )
        if 0 <= artist_selection < len(search_results["artists"]["items"]):
            artist_id = search_results["artists"]["items"][artist_selection]["id"]
            recommendations = recommend_artists(access_token, [artist_id], limit)
            print("Related Artists:", json.dumps(recommendations, indent=4))
        else:
            print("Invalid selection.")

    else:
        print("No results found.")


if __name__ == "__main__":
    main()
