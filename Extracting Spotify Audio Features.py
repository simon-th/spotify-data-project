# # Part 1: Extracting Audio Features From Spotify Playlist

# ## 1. Setting Up

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

credentials = json.load(open('credentials.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

playlist_index = 0

playlists = json.load(open('playlists.json'))
playlist_uri = playlists[playlist_index]['uri']
like = playlists[playlist_index]['like']

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# ## 2. Extracting Track Information from Playlist

uri = playlist_uri    # the URI is split by ':' to get the username and playlist ID
username = uri.split(':')[2]
playlist_id = uri.split(':')[4]
results = sp.user_playlist(username, playlist_id, 'tracks')

# ## 3. Extracting  IDs, Titles, and Artists

playlist_tracks_data = results['tracks']
playlist_tracks_id = []
playlist_tracks_titles = []
playlist_tracks_artists = []
playlist_tracks_first_artists = []

for track in playlist_tracks_data['items']:
    playlist_tracks_id.append(track['track']['id'])
    playlist_tracks_titles.append(track['track']['name'])
    # adds a list of all artists involved in the song to the list of artists for the playlist
    artist_list = []
    for artist in track['track']['artists']:
        artist_list.append(artist['name'])
    playlist_tracks_artists.append(artist_list)
    playlist_tracks_first_artists.append(artist_list[0])

# ## 4. Extracting Audio Features from Each Track

features = sp.audio_features(playlist_tracks_id)

import numpy as np
import pandas as pd

features_df = pd.DataFrame(data=features, columns=features[0].keys())

# ## 5. Merging Audio Features with Track Information

features_df['title'] = playlist_tracks_titles
features_df['first_artist'] = playlist_tracks_first_artists
features_df['all_artists'] = playlist_tracks_artists
features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                           'danceability', 'energy', 'key', 'loudness',
                           'mode', 'acousticness', 'instrumentalness',
                           'liveness', 'valence', 'tempo',
                           'duration_ms', 'time_signature']]
features_df.head()

# ## 6. Initial Data Exploration

import matplotlib.pyplot as plt
import seaborn as sns
#get_ipython().run_line_magic('matplotlib', 'inline')

sns.pairplot(features_df)

plt.figure(figsize=(64,6))
sns.countplot(features_df['first_artist'])

features_df = features_df.drop(['first_artist', 'all_artists'], axis=1)

features_df.head()

# ## 7. Additional Data from Audio Analysis

num_bars = []
num_sections = []
num_segments = []

for i in range(0,len(features_df['id'])):
    analysis = sp.audio_analysis(features_df.iloc[i]['id'])
    num_bars.append(len(analysis['bars'])) # beats/time_signature
    num_sections.append(len(analysis['sections']))
    num_segments.append(len(analysis['segments']))
    # print(len(analysis['tatums'])) # beats*2
    # print(len(analysis['beats'])) # tempo*minutes

plt.figure(figsize=(16,4))
plt.subplot(1,3,1)
plt.hist(num_bars, bins=20)
plt.xlabel('num_bars')
plt.subplot(1,3,2)
plt.hist(num_sections, bins=20)
plt.xlabel('num_sections')
plt.subplot(1,3,3)
plt.hist(num_segments, bins=20)
plt.xlabel('num_segments')

features_df['num_bars'] = num_bars
features_df['num_sections'] = num_sections
features_df['num_segments'] = num_segments
features_df.head()

# ## 8. Classifying Tracks

if like == True:
    features_df['class'] = np.ones((len(features_df), 1), dtype=int)
else:
    features_df['class'] = np.zeros((len(features_df), 1), dtype=int)

features_df.head()

# ## 9. Exporting JSON File

filename = 'playlist' + str(playlist_index) + '.json'
features_df.to_json(filename)

