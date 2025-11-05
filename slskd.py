import slskd_api
import time

from creds import SLSKD_API_KEY


class Slskd:
    def __init__(self, host: str, api_key: str):
        self.slskd = slskd_api.SlskdClient(host, api_key)

    # Выполняет поиск песни. Возвращает словарь с результатами поиска
    def search_song(self, query, maxQueue=10):
        search = self.slskd.searches.search_text(query, maximumPeerQueueLength=maxQueue)
        while True:
            if self.slskd.searches.state(search["id"])["isComplete"]:
                return self.slskd.searches.search_responses(search["id"])


    # Выполняет фильтрацию результата поиска в соответствии с заданными параметрами.
    # При успехе возвращает кортеж target. При ошибке возвращает 1
    def choose_song(self, search: dict, codec="mp3", loadOtherCodec=True):
        if search == []:
            return 1

        target=""
        for user in search:
            for file in user["files"]:
                if f".{codec}" in file["filename"]:
                    target = (user["username"], file)
                    break
            if target !="":
                break

        if target =="" and loadOtherCodec:
            target = (search[0]["username"], search[0]["files"][0])
            return target
        elif target != "":
            return target
        else:
            return 1

    def download_song(self, target):
        if target == 1:
            print("song not found")
            return

        print(target)
        username, file = target
        self.slskd.transfers.enqueue(username=username, files=[file])
        downloads = self.slskd.transfers.get_downloads(username)

        d_id=""
        for dir in downloads["directories"]:
            if d_id != "":
                break
            for dir_file in dir["files"]:
                if d_id != "":
                    break
                if dir_file["filename"] == file["filename"]:
                    d_id = dir_file["id"]
                    break
        while True:
            state = self.slskd.transfers.get_download(username, d_id)["state"]
            if state == "Completed, Succeeded":
                print(f"download {file["filename"]} complited!")
                break
            if state == "Completed, Errored":
                print(f"{file["filename"]} download error!")
                break
            time.sleep(5)


    def get_song(self, query, maxQueue=10):
        return self.download_song(self.choose_song(self.search_song(query, maxQueue)))




t = Slskd("http://127.0.0.1:5030", SLSKD_API_KEY)
songs = ["Cartridge1987 MFOS"]
for song in songs:
    t.get_song(song)