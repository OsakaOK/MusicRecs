# Music Recommendation System

This is a Flask-based music recommendation system that uses the Spotify API.

## Features

- Search for tracks and artists
- Get recommendations based on tracks and artists

## Requirements

- Python 3.x
- Spotify Developer Account

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/MusicRecs.git
   cd MusicRecs
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**:

   - Create a `.env` file in the root directory of the project.
   - Copy the contents of `.env.example` to `.env`.
   - Fill in your Spotify Client ID and Client Secret in the `.env` file.

   ```plaintext
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```

5. **Run the application**:

   ```bash
   flask run
   ```

6. **Open your browser**:
   - Visit `http://127.0.0.1:5000` to use the application.

## Usage

- Enter the track or artist name in the search box.
- Select the type (Track or Artist).
- Click "Search" to get results.
- Click "Get Recommendations" to get recommendations based on the selected track or artist.
