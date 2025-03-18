import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import requests


SPOTIFY_CLIENT_ID = "3dc27a5db2f44f0ebaf996c15ea04b1e"
SPOTIFY_CLIENT_SECRET = "19eec47a6d13467da89b521612b0259f"
SPOTIFY_REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "user-library-read playlist-read-private user-read-private user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read"
USERNAME = "ze4op3dkz3gqbcc4nluk9fyvc"

auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    username=USERNAME,
    open_browser=True
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def get_user_playlists():
    playlists = sp.current_user_playlists()
    playlist_data = []
    
    for playlist in playlists['items']:
        playlist_data.append({
            "playlist_name": playlist['name'],
            "playlist_id": playlist['id'],
            "total_tracks": playlist['tracks']['total']
        })

    return playlist_data


def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    
    for item in results['items']:
        track = item['track']
        track_data = {
            "id": track["id"],
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "playlist_id": playlist_id,
            "features": get_audio_features(track["id"])
        }
        tracks.append(track_data)
    
    return tracks


def get_audio_features(track_id):
    try:
        if not sp.auth_manager.get_cached_token():
            print("Token not found or expired, re-authenticating...")
            sp.auth_manager.get_access_token(as_dict=False)
            
        features = sp.audio_features(track_id)
        if features and features[0]:
            return {
                "danceability": features[0]["danceability"],
                "energy": features[0]["energy"],
                "valence": features[0]["valence"],
                "tempo": features[0]["tempo"]
            }
        else:
            print(f"No features found for track {track_id}")
    except Exception as e:
        print(f"Error getting features for track {track_id}: {e}")
    
    return {
        "danceability": None,
        "energy": None,
        "valence": None,
        "tempo": None
    }

def collect_all_playlist_data():
    playlists = get_user_playlists()
    all_tracks = []
    
    for playlist in playlists:
        print(f"Fetching tracks from playlist: {playlist['playlist_name']} ({playlist['total_tracks']} tracks)")
        tracks = get_playlist_tracks(playlist["playlist_id"])
        all_tracks.extend(tracks)

    return all_tracks


def save_data_to_dataframe():
    data = collect_all_playlist_data()
    df = pd.DataFrame(data)

    # features_df = df["features"].apply(pd.Series)
    # df = df.drop(columns=["features"]).join(features_df)

    df.to_csv("spotify_playlist_data.csv", index=False)
    print("Data saved to spotify_playlist_data.csv!")

    auth_manager.cache_handler.clear()
    sp.auth_manager.cache_handler.clear()
    save_data_to_dataframe()


if __name__ == "__main__":
    token_info = sp.auth_manager.get_access_token(as_dict=True)
    print(f"Access token obtained: {token_info['access_token'][:5]}... (expires in {token_info['expires_in']} seconds)")

    # song_id = "3n3PpFg5vCwsn9ZXxiJdZ0"


    # song_attributes = get_audio_features(song_id)
    # print(song_attributes)


    token_info = sp.auth_manager.get_access_token(as_dict=True)
    print(f"Access token obtained: {token_info['access_token'][:5]}... (expires in {token_info['expires_in']} seconds)")
        
    save_data_to_dataframe()