import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

clientID = '' # Introducir credenciales
clientSecret = '' # Introducir credenciales
auth_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
num_track_per_year = 1000

sp = spotipy.Spotify(auth_manager=auth_manager)

# Búsqueda de canciones lanzadas en en rango 
year_start = 2020
year_end = 2024
track_data = []
for year in range(year_start, year_end):
    # Por cada año se añade un numero determinado de canciones
    for j in range (0, num_track_per_year, 50):
        # Canciones lanzados en este año
        results = sp.search(q=f'year:{year}', type='track', limit=50, offset= j)
        # Info basico
        track_ids = [item['id'] for item in results['tracks']['items']]
        # info más avanzados
        track_details = sp.audio_features(tracks=track_ids)
        # Se hace un filtro de campos interesados
        for i, track in enumerate(track_details):
            info = results['tracks']['items'][i]
            track_artists = [artist['name'] for artist in info['artists']]
            # Aplico un filtro extra de popularity para eliminar algunos duplicados observados
            if track and info['popularity'] > 10:
                track_row = [track['valence'], year, track['acousticness'], track_artists, 
                            track['danceability'],track['duration_ms'], track['energy'],
                            info['explicit'], track['id'], track['instrumentalness'], track['key'],
                            track['liveness'], track['loudness'], track['mode'], info['name'], 
                            info['popularity'], info['album']['release_date'], track['speechiness'], track['tempo'] ]
                track_data.append(track_row)

# Generación de csv
with open('spotify_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Escribir la fila de encabezado
    header = ['valence', 'year', 'acousticness', 'artists', 'danceability', 'duration_ms', 'energy', 
            'explicit', 'id', 'instrumentalness','key', 'liveness', 'loudness', 'mode', 'name', 
            'popularity', 'release date', 'speechiness', 'tempo']
    csvwriter.writerow(header)
    # Escribir los datos
    csvwriter.writerows(track_data)