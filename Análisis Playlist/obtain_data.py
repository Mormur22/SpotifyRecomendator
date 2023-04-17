import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

clientID = '' # Introducir credenciales
clientSecret = '' # Introducir credenciales
nombre_usuario = '' # Rellenar con el nombre de usuario del que se quiera sacar informacion
auth_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)

sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = []
playlistsID = []
def get_user_playlist(username):
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        playlistsID.append(playlist['id'])
        print("Name: {}, Number of songs: {}, Playlist ID: {} ".
              format(playlist['name'].encode('utf8'),
                     playlist['tracks']['total'],
                     playlist['id']))
    
def get_content_playlist(username, playlist_id):
    offset = 0
    songs = []
    while True:
        content = sp.user_playlist_tracks(username, playlist_id, fields=None,
                                          limit=100, offset=offset, market=None)
        songs += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break
    print(songs)
  

songs = []
audio_features = []
features_list = []
def get_playlist_audio_features(username, playlist_id):
    ids = []
    offset = 0
    songsAux = []
    while True:
        content = sp.user_playlist_tracks(username, playlist_id, fields=None, limit=100, offset=offset, market=None)
        songsAux += content['items']
        if content['next'] is not None:
            offset += 100
        else:
            break

    for i in songsAux:
        ids.append(i['track']['id'])

    index = 0
    audio_featuresAux = []
    while index < len(ids):
        audio_featuresAux += sp.audio_features(ids[index:index + 50])
        index += 50

    for features in audio_featuresAux:
        if features is not None: 
            song_uri = features['uri']
            song_info = sp.track(song_uri)
            features_list.append([features['energy'], features['liveness'],
                                features['tempo'], features['speechiness'],
                                features['acousticness'], features['instrumentalness'],
                                features['time_signature'], features['danceability'],
                                features['key'], features['duration_ms'],
                                features['loudness'], features['valence'],
                                features['mode'], features['uri'], song_info['name'], song_info['artists'][0]['name']])
        else: 
            features_list.append([0.5, 0.5, 140 , 0.5, 0.5, 0.5, 5, 0.5, 5, 200000, -15, 0.5, 1, 'no link', 'no name', 'no artist'])

    print(len(features_list))
    
def toCSV(features_list, username):
    df = pd.DataFrame(features_list, columns=['energy', 'liveness',
                                              'tempo', 'speechiness',
                                              'acousticness', 'instrumentalness',
                                              'time_signature', 'danceability',
                                              'key', 'duration_ms', 'loudness',
                                              'valence', 'mode', 'uri', 'name', 'artist'])
    df.to_csv('{}-playlists.csv'.format(username), index=False)




get_user_playlist(nombre_usuario)
print(len(playlistsID))
for i in playlistsID:
    get_playlist_audio_features(nombre_usuario, i)
toCSV(features_list, nombre_usuario)



