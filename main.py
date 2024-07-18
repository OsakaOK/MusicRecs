import requests
import base64
import json
from SpotifyAPI import (
    get_access_token,
    search_spotify,
    get_recommendations,
    get_related_artists,
    clean_track_data,
    clean_artist_data,
    cache_recommendations,
    cache_search_results,
    get_cached_recommendations,
    get_cached_search_results,
)

# Spotify API credentials
client_id = "5ec05cefccd647058cffeac2d91dc387"
client_secret = "65e2c4321945442ba9eed181ee529548"


def main():
    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        print("Failed to obtain access token.")
        return

    while True:
        query = input("Enter the name of the track or artist: ")
        search_type = input("Enter the type (track or artist): ").lower()
        search_limit = int(input("Enter the number of search results to display: "))
        recommend_limit = int(input("Enter the number of recommendations to fetch: "))

        if search_type not in ["track", "artist"]:
            print("Invalid search type. Only 'track' and 'artist' are supported.")
            continue

        cached_results = get_cached_search_results(search_type, query)
        if cached_results:
            search_results = cached_results
        else:
            search_results = search_spotify(
                access_token, query, search_type, limit=search_limit
            )
            cache_search_results(search_type, query, search_results)

        if (
            search_type == "track"
            and "tracks" in search_results
            and "items" in search_results["tracks"]
            and search_results["tracks"]["items"]
        ):
            print("Search Results:")
            unique_tracks = clean_track_data(search_results["tracks"]["items"])
            for idx, track in enumerate(unique_tracks):
                track_name = track["name"]
                artist_names = ", ".join(track["artists"])
                print(f"{idx + 1}: {track_name} by {artist_names}")

            track_selection = (
                int(
                    input(
                        "Enter the number of the track you want recommendations for: "
                    )
                )
                - 1
            )
            if 0 <= track_selection < len(unique_tracks):
                track_id = unique_tracks[track_selection]["id"]

                cached_recommendations = get_cached_recommendations(track_id)
                if cached_recommendations:
                    recommendations = cached_recommendations
                else:
                    recommendations = get_recommendations(
                        access_token, [track_id], recommend_limit
                    )
                    cache_recommendations(track_id, recommendations)

                cleaned_recommendations = clean_track_data(recommendations["tracks"])
                print(
                    "Recommended Tracks:", json.dumps(cleaned_recommendations, indent=4)
                )
            else:
                print("Invalid selection.")

        elif (
            search_type == "artist"
            and "artists" in search_results
            and "items" in search_results["artists"]
            and search_results["artists"]["items"]
        ):
            print("Search Results:")
            unique_artists = clean_artist_data(search_results["artists"]["items"])
            for idx, artist in enumerate(unique_artists):
                artist_name = artist["name"]
                print(f"{idx + 1}: {artist_name}")

            artist_selection = (
                int(
                    input(
                        "Enter the number of the artist you want recommendations for: "
                    )
                )
                - 1
            )
            if 0 <= artist_selection < len(unique_artists):
                artist_id = unique_artists[artist_selection]["id"]
                related_artists = get_related_artists(
                    access_token, artist_id, recommend_limit
                )
                cleaned_related_artists = clean_artist_data(related_artists)
                print("Related Artists:", json.dumps(cleaned_related_artists, indent=4))
            else:
                print("Invalid selection.")

        else:
            print("No results found.")

        cont = input("Do you want to search again? (yes/no): ").strip().lower()
        if cont != "yes":
            break


if __name__ == "__main__":
    main()
