# Import necessary libraries 
import pandas as pd 
import streamlit as st 
import time 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Perform authentication (ADD YOUR CREDENTIALS HERE)
client_id = "cbf123007b33453cb4218e9a25e13f4c"
client_secret = "4398a3bfb2c044f595841eba30b63556"

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Authenticate the spotify API 


## Utility Functions 

# Function to get the tracks from a playlist    
def get_playlist_tracks(playlist_id):
    """Function to get the tracks from a playlist

    Args:
        playlist_id (str): ID of the playlist

    Returns:
        list: List of track IDs
    """
    
    playlist_tracks = sp.playlist(playlist_id, additional_types=('track',))

    track_ids = []
    for item in playlist_tracks["tracks"]["items"]:
        track = item["track"]
        track_ids.append(track["id"])
    
    return track_ids

# Function to get the features of the track based on ID
def get_single_track_features(id):
    """
    Function to get the features and other information of a single track.
    """

    meta = sp.track(id)
    features = sp.audio_features(id)

    # Get the metadata of the track
    name = meta["name"]
    album = meta["album"]["name"]
    artist = meta["album"]["artists"][0]["name"]
    release_date = meta["album"]["release_date"]
    length = meta["duration_ms"]
    popularity = meta["popularity"]
    genres = meta["artists"]

    # Get the audio Features of the track
    acousticness = features[0]["acousticness"]
    key = features[0]["key"]
    danceability = features[0]["danceability"]
    energy = features[0]["energy"]
    instrumentalness = features[0]["instrumentalness"]
    liveness = features[0]["liveness"]
    loudness = features[0]["loudness"]
    speechiness = features[0]["speechiness"]
    tempo = features[0]["tempo"]
    time_signature = features[0]["time_signature"]
    mode = features[0]["mode"]
    valence = features[0]["valence"]
    # Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

    return [
        name,
        album,
        artist,
        release_date,
        length,
        popularity,
        key,
        danceability,
        acousticness,
        danceability,
        energy,
        instrumentalness,
        liveness,
        loudness,
        speechiness,
        tempo,
        valence,
        time_signature,
        mode,
    ]

# Function to create a dataframe of track information
def create_track_features_dataframe(tracks: list):
    """Function to generate a dataframe of song features from a list of songs

    Args:
        tracks (list): List of songs to make a dataframe of

    Returns:
        pandas.DataFrame: Dataframe of song features
    """

    # Iterate through the list of tracks
    all_track_data = []
    for track in tracks:
        time.sleep(0.5)
        track_data = get_single_track_features(track)
        all_track_data.append(track_data)

    return pd.DataFrame(
        all_track_data,
        columns=[
            "name",
            "album",
            "artist",
            "release_date",
            "length",
            "popularity",
            "key",
            "danceability",
            "acousticness",
            "danceability",
            "energy",
            "instrumentalness",
            "liveness",
            "loudness",
            "speechiness",
            "tempo",
            "valence",
            "time_signature",
            "mode",
        ],
    )

## Streamlit app design 

st.title("Streamlit Data Collection using Playlist")

# Get the playlist ID as an input 
playlist_id = st.text_input("Enter the playlist ID")

if st.button("Get data"): 
    print("Collecting data for the playlist - " + playlist_id)
    song_ids = get_playlist_tracks(playlist_id=playlist_id)
    playlist_data = create_track_features_dataframe(song_ids)

    st.dataframe(playlist_data)