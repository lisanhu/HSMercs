import requests as req
import json
import time
import threading


class DownloadClient(threading.Thread):
    def __init__(self, url, pos, data_store):
        threading.Thread.__init__(self)
        self.url = url
        self.pos = pos
        self.data = data_store
    
    def run(self):
        # print("Downloading page {}...".format(self.pos + 1))
        res = req.get(self.url).json()["leaderboard"]["rows"]
        assert(len(self.data) > self.pos)
        self.data[self.pos] = res


def download_leaderboard_data(path: str) -> list:
    root_url = "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=US&leaderboardId=mercenaries"
    resp = req.get(root_url)
    resp = resp.json()

    current_season = resp["seasonMetaData"]["US"]["mercenaries"]["seasons"][0]
    total_pages = resp["leaderboard"]["pagination"]["totalPages"]

    print("Current seasonId is {}, total pages: {}".format(current_season, total_pages))
    start_time = time.time()
    data_store = [[]] * total_pages
    threads = []
    for pg in range(total_pages):
        url = root_url + "&seasonId={}&page={}"
        url = url.format(current_season, pg + 1)
        t = DownloadClient(url, pg, data_store)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    
    end_time = time.time()
    print("Done downloading. Time taken {} seconds.".format(end_time - start_time))

    rows = []
    for page_data in data_store:
        rows += page_data

    if path != None:
        with open(path, "w") as db:
            db.write(json.dumps(rows))
        print("Done writing to file {}".format(path))

    return rows

if __name__ == "__main__":
    print(download_leaderboard_data(None))
