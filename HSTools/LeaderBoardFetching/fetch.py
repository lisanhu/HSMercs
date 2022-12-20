import requests as req
import json
import time

def single_download_task(url: str) -> list:
    return req.get(url).json()["leaderboard"]["rows"]

def download_leaderboard_data(path: str) -> list:
    root_url = "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=US&leaderboardId=mercenaries"
    resp = req.get(root_url)
    resp = resp.json()

    current_season = resp["seasonMetaData"]["US"]["mercenaries"]["seasons"][0]
    total_pages = resp["leaderboard"]["pagination"]["totalPages"]
    rows = []

    print("Current seasonId is {}, total pages: {}".format(current_season, total_pages))
    start_time = time.time()
    for pg in range(total_pages):
        url = root_url + "&seasonId={}&page={}"
        url = url.format(current_season, pg + 1)
        print("Downloading page {}...".format(pg + 1))
        resp = req.get(url).json()
        rows = rows + resp["leaderboard"]["rows"]
    
    end_time = time.time()
    print("Done downloading. Time taken {} seconds.", end_time - start_time)

    with open(path, "w") as db:
        db.write(json.dumps(rows))
    print("Done writing to file {}".format(path))

    return rows

if __name__ == "__main__":
    download_leaderboard_data("leaderboard.data")
