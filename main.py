from json import load
import os
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import random

load_dotenv()

cid = os.getenv('CLIENT_ID')
secret = os.getenv('CLIENT_SECRET')

#Authentication - user-generic
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlist_links = ["https://open.spotify.com/playlist/6UeSakyzhiEt4NB3UAd6NQ?si=f510b76c45134297", 
"https://open.spotify.com/playlist/5ABHKGoOzxkaa28ttQV9sE?si=18693cf0baf54b12"]

playlist_uris = [playlist_link.split("/")[-1].split("?")[0] for playlist_link in playlist_links] 

track_uris = []

for uri in playlist_uris:
    for x in sp.playlist_tracks(uri)["items"]:
        track_uris.append(x["track"]["uri"])


mood = (int)(input("What\'s your mood on a scale of 1 to 10? \n(10 is you're having the best day of your life)\n"))

songs = []


random.shuffle(track_uris)
for t in track_uris: 
    if len(songs) == 5:
        break
    f = sp.audio_features(t)[0]
    try: 
        if 1 <= mood < 2:
            if 0 <= f['valence'] < 0.2 and 0 <= f['energy'] < 0.2:
                songs.append(f['uri'])
        elif 2 <= mood < 4:
            if 0.2 <= f['valence'] < 0.4 and 0.2 <= f['energy'] < 0.4:
                songs.append(f['uri'])
        elif 4 <= mood < 6:
            if 0.4 <= f['valence'] < 0.6 and 0.4 <= f['energy'] < 0.6:
                songs.append(f['uri'])
        elif 6 <= mood < 8:
            if 0.6 <= f['valence'] < 0.8 and 0.6 <= f['energy'] < 0.8:
                songs.append(f['uri'])
        else:
            if 0.8 <= f['valence'] < 1 and 0.8 <= f['energy'] < 1:
                songs.append(f['uri'])
    except TypeError as te:
        continue

if len(songs) < 3:
    print("sorry bro")
else:
    for i,uri in enumerate(songs):
        print(str(i+1) + ". " + sp.track(uri)['name'] + ' -- ' + sp.track(uri)['artists'][0]['name'])