# Spotify Data Project

In this project, I extracted data from my Spotify playlists using Spotify API and used it to predict if I will like a certain song or not.

The main purpose of this project was to make myself more familiar with the process of working with data and using the Numpy, Pandas, Seaborn, SciKit Learn and TensorFlow libraries in Python.

This repository contains three Jupyter Notebooks that document my work:

Part 1 - [Extracting Spotify Audio Features](https://github.com/simon-th/spotify-data-project/blob/master/Extracting%20Spotify%20Audio%20Features.ipynb)

Parts 2 and 3 - [Exploring Playlist Data and Learning Models](https://github.com/simon-th/spotify-data-project/blob/master/Exploring%20Playlist%20Data%20and%20Learning%20Models.ipynb)

Part 4 - [Predictions on Separate Dataset](https://github.com/simon-th/spotify-data-project/blob/master/Predictions%20on%20Separate%20Dataset.ipynb)


The playlist data that I used is in a separate directory in the repository, but it needs to be in the same directory as the notebooks in order for the code to work.

This repository also includes the 'extractor.py' script that can create .json files based on your own playlists. The .json files can then be imported into a Pandas dataframe that contains the song title, unique ID and audio information.
To do this:
1. Follow the instructions on the [Spotipy documentation page](https://spotipy.readthedocs.io/en/latest/#authorized-requests) to get your credentials for the credentials.json file.
2. Open the Spotify playlist (of no more than 100 songs), click on the cirlce with three dots, go to Share -> Copy Spotify URI
3. Paste that Spotify URI in the playlists.json file in next to the key 'uri'.
4. If you want to classify the playlist by whether you like it or not, set the 'like' key to true or false.
5. Add or remove playlists as you please.
6. Run the script. (it should take 2-3 minutes per playlist)

