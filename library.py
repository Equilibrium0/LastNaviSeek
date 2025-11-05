import subprocess
from Song import Song


class Manager:
    def trackInLibrary(track:Song):
        return subprocess.run(['beet', 'ls', f'title:{track.title}', f'artist:{track.artist}',
                               f'album:{track.album}'], capture_output=True, text=True).stdout != ""

i = Song("Night of the Long Knives", "AC/DC", "For Those About To Rock")
print(Manager.trackInLibrary(i))