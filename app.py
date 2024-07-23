from flask import Flask, request, jsonify, render_template
from SpotifyAPI import (
    get_access_token,
    search_spotify,
    get_recommendations,
    get_related_artists,
    clean_track_data,
    clean_artist_data,
    cache_search_results,
    get_cached_search_results,
    cache_recommendations,
    get_cached_recommendations,
    client_id,
    client_secret,
    connect_to_mongo,
)
from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address, app=app, default_limits=["200 per day", "50 per hour"]
)

app = Flask(__name__)

# MongoDB connection
db = connect_to_mongo()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
@limiter.limit("10 per minute")
def search():
    query = request.form["query"]
    search_type = request.form["search_type"]

    # Validate search_limit
    try:
        search_limit = int(request.form["search_limit"])
        if search_limit <= 0:
            return jsonify({"error": "Search limit must be a positive integer."}), 400
    except ValueError:
        return jsonify({"error": "Search limit must be a valid integer."}), 400

    if search_type not in ["track", "artist"]:
        return (
            jsonify(
                {
                    "error": "Invalid search type. Only 'track' and 'artist' are supported."
                }
            ),
            400,
        )

    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        return jsonify({"error": "Failed to obtain access token."}), 500

    cached_results = get_cached_search_results(db, search_type, query, search_limit)
    if cached_results:
        search_results = cached_results
    else:
        search_results = search_spotify(
            access_token, query, search_type, limit=search_limit
        )
        cache_search_results(db, search_type, query, search_limit, search_results)

    if (
        search_type == "track"
        and "tracks" in search_results
        and "items" in search_results["tracks"]
        and search_results["tracks"]["items"]
    ):
        unique_tracks = clean_track_data(search_results["tracks"]["items"])
        return jsonify(unique_tracks)

    elif (
        search_type == "artist"
        and "artists" in search_results
        and "items" in search_results["artists"]
        and search_results["artists"]["items"]
    ):
        unique_artists = clean_artist_data(search_results["artists"]["items"])
        return jsonify(unique_artists)

    return jsonify({"error": "No results found."}), 404


@app.route("/recommend", methods=["POST"])
@limiter.limit("10 per minute")
def recommend():
    item_type = request.form["item_type"]
    item_id = request.form["item_id"]

    print(
        f"Received request for recommendations: item_type={item_type}, item_id={item_id}"
    )

    # Validate recommend_limit
    try:
        recommend_limit = int(request.form["recommend_limit"])
        if recommend_limit <= 0:
            return (
                jsonify({"error": "Recommend limit must be a positive integer."}),
                400,
            )
    except ValueError:
        return jsonify({"error": "Recommend limit must be a valid integer."}), 400

    access_token = get_access_token(client_id, client_secret)
    if not access_token:
        return jsonify({"error": "Failed to obtain access token."}), 500

    if item_type == "track":
        cached_recommendations = get_cached_recommendations(db, item_id)
        if cached_recommendations:
            recommendations = cached_recommendations
        else:
            recommendations = get_recommendations(
                access_token, [item_id], recommend_limit
            )
            if recommendations is None:
                return jsonify({"error": "Failed to fetch track recommendations."}), 500
            cache_recommendations(db, item_id, recommendations)

        cleaned_recommendations = clean_track_data(recommendations["tracks"])
        return jsonify(cleaned_recommendations)

    elif item_type == "artist":
        related_artists = get_related_artists(access_token, item_id, recommend_limit)
        if related_artists is None:
            return jsonify({"error": "Failed to fetch related artists."}), 500
        cleaned_related_artists = clean_artist_data(related_artists)
        return jsonify(cleaned_related_artists)

    return (
        jsonify(
            {"error": "Invalid item type. Only 'track' and 'artist' are supported."}
        ),
        400,
    )


if __name__ == "__main__":
    app.run(debug=True)
