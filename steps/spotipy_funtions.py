import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify client items:
client_id = "ef77e31c5d4049818901058b81bd56a3"
client_secret = "c773be9c070044e2ad067db5f86b62cb"
uri = "http://localhost:8080"
# Endpoint
token_url = "https://accounts.spotify.com/api/token"
# Initialize the Spotify authentication client
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# Create a Spotify object, for  requesting
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_playlist_id(playlist_name):
    """
    Get the ID of a Spotify playlist with the given name.

    Parameters:
        playlist_name (str): The name of the playlist to search for.

    Returns:
        str: The ID of the playlist, or None if the playlist is not found.
    """

    # Perform the search for the playlist by its name
    results = sp.search(q=playlist_name, type='playlist')

    # Check if any playlists were found
    if results['playlists']['items']:
        # Iterate over each search result
        for item in results['playlists']['items']:
            # Check if the owner is Spotify
            if item['owner']['id'] == 'Spotify' or item['owner']['id'] == 'spotify':
                # Return the ID of the playlist
                return item['id']

    # Print a message if the playlist is not found
    print("Playlist '{}' not found.".format(playlist_name))
    return None

def get_playlist_info(playlist_id):
    try:
        # Use the playlist() function from Spotipy to retrieve playlist information
        playlist_info = sp.playlist(playlist_id)
        return playlist_info
    except spotipy.SpotifyException as e:
        print("Error getting playlist information:", e)
        return None
    
def get_playlist_data(playlist_id):
    playlist_info = get_playlist_info(playlist_id)
    if playlist_info:
        followers = playlist_info['followers']['total']
        total_songs = playlist_info['tracks']['total']
        return pd.Series({'followers': followers, 'total_songs': total_songs})
    else:
        return pd.Series({'followers': None, 'total_songs': None})
    
def create_playlist_df(playlist_dataframe, country):
    playlist_id_series = playlist_dataframe.loc[playlist_dataframe['country'] == country]["playlist_id"]
    
    # Check if playlist_id_series is empty
    if playlist_id_series.empty:
        print("Playlist not found for the country:", country)
        return None
    
    playlist_id = playlist_id_series.iloc[0]  # Extract the playlist ID from the Series
    playlist_info = get_playlist_info(playlist_id)

    if not playlist_info:
        print("Error: Playlist information not found for ID:", playlist_id)
        return None
    
    owner = playlist_info['owner']['display_name']
    
    # Check if the owner is Spotify (case insensitive)
    if owner.lower() != "spotify":
        print("Playlist not owned by Spotify. Skipping...")
        return None
    
    tracks = playlist_info['tracks']['items']
    playlist_data = []

    for track in tracks:
        artist = track['track']['artists'][0]['name']
        album = track['track']['album']['name']
        song_name = track['track']['name']
        release_date = track['track']['album']['release_date']
        duration_ms = track['track']['duration_ms']
        popularity = track['track']['popularity']
        track_id = track['track']['id']

        playlist_data.append({
            'country': country,
            'artist': artist,
            'album': album,
            'song_name': song_name,
            'release_date': release_date,
            'duration_ms': duration_ms,
            'popularity': popularity,
            'track_id': track_id
        })

    playlist_df = pd.DataFrame(playlist_data)
    return playlist_df

def get_audio_features(track_id):
    # Retrieve the audio features of the song using the track_id
    audio_features = sp.audio_features(track_id)
    return audio_features[0] if audio_features else None