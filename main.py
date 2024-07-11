import requests
import base64
import json
from SpotifyAPI import (
    get_access_token,
    fetch_track_info,
    fetch_artist_info,
    fetch_album_info,
    search_spotify,
)

# Spotify API credentials
client_id = "5ec05cefccd647058cffeac2d91dc387"
client_secret = "65e2c4321945442ba9eed181ee529548"


def main():
    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        print("Failed to obtain access token.")
        return

    query = input("Enter the name of the track, artist, or album: ")
    search_type = input("Enter the type (track, artist, album): ").lower()

    search_results = search_spotify(access_token, query, search_type)

    if search_type == "track" and search_results["tracks"]["items"]:
        track_id = search_results["tracks"]["items"][0]["id"]
        track_data = fetch_track_info(access_token, track_id)
        print("Track Data:", json.dumps(track_data, indent=4))

    elif search_type == "artist" and search_results["artists"]["items"]:
        artist_id = search_results["artists"]["items"][0]["id"]
        artist_data = fetch_artist_info(access_token, artist_id)
        print("Artist Data:", json.dumps(artist_data, indent=4))

    elif search_type == "album" and search_results["albums"]["items"]:
        album_id = search_results["albums"]["items"][0]["id"]
        album_data = fetch_album_info(access_token, album_id)
        print("Album Data:", json.dumps(album_data, indent=4))

    else:
        print("No results found.")


if __name__ == "__main__":
    main()
