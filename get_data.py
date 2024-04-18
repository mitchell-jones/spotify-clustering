from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import spotipy
import pandas as pd
from pathlib import Path


def authenticate():
    load_dotenv()
    scope = 'user-library-read playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp

def get_target_playlist_id_and_length(sp):
    # prerequisite for this step
    # download Spotify Desktop, and create a playlist called "Total Liked Songs"
    # then open your liked songs, hit ctrl+A, then drag all of your liked songs into this playlist
    # this is how we ingest all of your liked songs, since there is no 

    total_playlists = sp.current_user_playlists(limit = 10)['total']
    if total_playlists < 50:
        user_playlists = sp.current_user_playlists(limit = 50)
    else:
        # TODO: add code to get playlist information piecewise
        pass

    # can substitute other playlist name rather than 'Total Liked Songs' for other purposes/projects
    target_playlist_name = 'Total Liked Songs'
    for playlist in user_playlists['items']:
        if playlist['name'] == target_playlist_name:
            user_liked_songs_playlist = playlist

    return user_liked_songs_playlist['id'], user_liked_songs_playlist['tracks']['total']

def get_info_on_tracks(sp, playlist_id, offset):
    response = sp.playlist_tracks(playlist_id, offset = offset)
    base_dict = {'track_id':[], 'name':[], 'preview_url':[]}
    for i in response['items']:
        base_dict['name'].append(i['track']['name'])
        base_dict['track_id'].append(i['track']['id'])
        base_dict['preview_url'].append(i['track']['preview_url'])
    base_df = pd.DataFrame.from_records(base_dict)
    features = sp.audio_features(base_dict['track_id'])
    features_df = pd.DataFrame(features)
    playlist_df = base_df.merge(features_df, left_on = 'track_id', right_on = 'id')
    return playlist_df

def get_data_in_chunks(sp, playlist_id, total_playlist_length):
    # calculate chunks
    offsets = list(range(100, total_playlist_length+1, 100)) # Needs to be dynamic if playlist length changes
    main_df = get_info_on_tracks(sp, playlist_id, offset = 0)

    # moving in chunks of 100
    for offset in offsets:
        df_new = get_info_on_tracks(sp, playlist_id, offset = offset)
        main_df = main_df.append(df_new)
    
    return main_df

def write_to_database():
    pass

def write_to_file(data, output_dir, output_name):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    data.to_pickle(f'{output_dir}/{output_name}.pkl')