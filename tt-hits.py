import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
load_dotenv()

# Set up Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Get Spotify's "Today's Top Hits" playlist
playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
results = sp.playlist(playlist_id)

# Create a list of tracks with their features
tracks_with_features = []

# Iterate through the tracks in the playlist
for idx, item in enumerate(results["tracks"]["items"]):
    track = item["track"]
    artist_name = track["artists"][0]["name"]
    song_title = track["name"]
    preview_url = track["preview_url"]

    # Get track features (including tempo)
    features = sp.audio_features(track["id"])[0]
    tempo = features["tempo"]

    # Add track information to the list
    tracks_with_features.append({
        "song_title": song_title,
        "artist_name": artist_name,
        "tempo": tempo,
        "preview_url": preview_url
    })

# Sort the tracks by tempo in descending order
sorted_tracks = sorted(tracks_with_features, key=lambda x: x["tempo"], reverse=True)

# Print the sorted tracks
for track in sorted_tracks:
    print(f"{track['song_title']} - {track['artist_name']} - Tempo: {track['tempo']} - Preview: {track['preview_url']}")