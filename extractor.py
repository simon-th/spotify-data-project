import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np
import pandas as pd

def exportData(playlists, index, sp):
    
    uri = playlists[index]['uri']
    like = playlists[index]['like']
    
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
    results = sp.user_playlist(username, playlist_id, 'tracks')

    print('playlist' + str(index) + ' read')

    playlist_tracks_data = results['tracks']
    playlist_tracks_id = []
    playlist_tracks_titles = []
    for track in playlist_tracks_data['items']:
        playlist_tracks_id.append(track['track']['id'])
        playlist_tracks_titles.append(track['track']['name'])

    print('playlist' + str(index) + ' track info extracted')

    features = sp.audio_features(playlist_tracks_id)
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['title'] = playlist_tracks_titles
    features_df = features_df[['id', 'title', 'danceability', 'energy', 'key', 'loudness', 'mode', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']]

    print('playlist' + str(index) + ' audio features extracted')

    num_bars = []
    num_sections = []
    num_segments = []

    for i in range(0,len(features_df['id'])):
        analysis = sp.audio_analysis(features_df.iloc[i]['id'])
        num_bars.append(len(analysis['bars']))
        num_sections.append(len(analysis['sections']))
        num_segments.append(len(analysis['segments']))

    features_df['num_bars'] = num_bars
    features_df['num_sections'] = num_sections
    features_df['num_segments'] = num_segments

    print('playlist' + str(index) + ' audio analysis info extracted')

    if like == True:
        features_df['class'] = np.ones((len(features_df), 1), dtype=int)
    else:
        features_df['class'] = np.zeros((len(features_df), 1), dtype=int)

    print('playlist' + str(index) + ' tracks classified')

    filename = 'playlist' + str(index) + '.json'
    features_df.to_json(filename)

    print('playlist' + str(index) + ' json file exported') 

# ## MAIN PROGRAM

credentials = json.load(open('credentials.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = json.load(open('playlists.json'))

for i in range(0, len(playlists)):
    exportData(playlists, i, sp)







