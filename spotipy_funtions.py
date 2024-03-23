import pandas as pd
import spotipy


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
    
    tracks = playlist_info['tracks']['items']
    playlist_data = []

    for track in tracks:
        artist = track['track']['artists'][0]['name']
        album = track['track']['album']['name']
        song_name = track['track']['name']
        release_date = track['track']['album']['release_date']
        duration_ms = track['track']['duration_ms']
        popularity = track['track']['popularity']

        playlist_data.append({
            'Country': country,
            'Artist': artist,
            'Album': album,
            'Song_name': song_name,
            'Release_date': release_date,
            'Duration_ms': duration_ms,
            'Popularity': popularity
        })

    playlist_df = pd.DataFrame(playlist_data)
    return playlist_df

# Create a function to retrieve the audio features of a song
def get_audio_features(track_id):
    # Retrieve the audio features of the song using the track_id
    audio_features = sp.audio_features(track_id)
    return audio_features[0] if audio_features else None