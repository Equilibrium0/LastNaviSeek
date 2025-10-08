import pylast
import random
from threading import Thread
from slskd import Slskd
from creds import LASTFM_API_SECRET, LASTFM_API_KEY, LASTFM_PASS, LASTFM_USER, SLSKD_API_KEY


network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
    username=LASTFM_USER,
    password_hash=pylast.md5(LASTFM_PASS),
)

me = pylast.User(LASTFM_USER, network)


wanted = pylast.Artist("Alan Walker", network, LASTFM_USER)

sim = wanted.get_similar()
print(sim)

choose_artists = random.sample(sim, 5)

print(choose_artists)
playlist = []

for artist in choose_artists:
    tracks = random.sample(artist.item.get_top_tracks(), 5)
    for track in tracks:
        playlist.append({
            "Title": f"{track.item.get_title()}",
            "Album": f"{track.item.get_album()}",
            "Artist": f"{artist.item.get_name()}"
        })

print(playlist)

soul = Slskd("http://127.0.0.1:5030", api_key=SLSKD_API_KEY)

download_threads=[]
for track in playlist:
    d = Thread(target=soul.get_song, args=(track["Artist"]+' '+track["Title"],))
    download_threads.append(d)

for thread in download_threads:
    thread.start()

for thread in download_threads:
    thread.join()
