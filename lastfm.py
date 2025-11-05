import pylast
import random
from threading import Thread

from beets.util import case_sensitive

from slskd import Slskd
from creds import LASTFM_API_SECRET, LASTFM_API_KEY, LASTFM_PASS, LASTFM_USER, SLSKD_API_KEY
from Song import Song


network = pylast.LastFMNetwork(
    api_key=LASTFM_API_KEY,
    api_secret=LASTFM_API_SECRET,
    username=LASTFM_USER,
    password_hash=pylast.md5(LASTFM_PASS),
)

me = pylast.User(LASTFM_USER, network)

def getTopTracks():
    return me.get_top_tracks(period=" 7day", limit=3)

def getSimTracks(track:pylast.TopItem):
    print(track.item.get_name())
    return track.item.get_similar(10)

def toSong(source):
    track = source.item
    return Song(
        title=track.title,
        artist=track.artist.name,
        album=track.get_album().title
    )

# wanted = pylast.Artist("Alan Walker", network, LASTFM_USER)
#
# sim = wanted.get_similar()
# print(sim)
#
# choose_artists = random.sample(sim, 5)
#
# print(choose_artists)
# playlist = []
#
# for artist in choose_artists:
#     tracks = random.sample(artist.item.get_top_tracks(), 5)
#     for track in tracks:
#         playlist.append({
#             "Title": f"{track.item.get_title()}",
#             "Album": f"{track.item.get_album()}",
#             "Artist": f"{artist.item.get_name()}"
#         })
#
# print(playlist)
#
# soul = Slskd("http://127.0.0.1:5030", api_key=SLSKD_API_KEY)
#
# download_threads=[]
# for track in playlist:
#     d = Thread(target=soul.get_song, args=(track["Artist"]+' '+track["Title"],))
#     download_threads.append(d)
#
# for thread in download_threads:
#     thread.start()
#
# for thread in download_threads:
#     thread.join()
