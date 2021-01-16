import spotipy
import spotipy.util as util
from credentials import *
from spotipy.oauth2 import SpotifyOAuth

token = util.prompt_for_user_token("tfbninja", "nonescope", client_id=id,
                                   client_secret=secret, redirect_uri='your-app-redirect-url')


def show_tracks(results):
    for i, item in enumerate(results['items']):
        track = item['track']
        print(
            "   %d %32.32s %s" %
            (i, track['artists'][0]['name'], track['name']))


scope = 'playlist-read-private'
sp = spotipy.Spotify(auth=token)

playlists = sp.current_user_playlists()
user_id = sp.me()['id']

for playlist in playlists['items']:
    if playlist['owner']['id'] == user_id:
        print()
        print(playlist['name'])
        print('  total tracks', playlist['tracks']['total'])

        results = sp.playlist(playlist['id'], fields="tracks,next")
        tracks = results['tracks']
        show_tracks(tracks)

        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks)
