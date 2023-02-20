import lyricsgenius
from rich import print

import os
from dotenv import load_dotenv
from gspreader import *


load_dotenv()


GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_SECRET = os.getenv("GENIUS_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
WEEZER_GENIUS_ID = '12925'

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

class GeniusSong:
    def __init__(self, title, genius_views):
        self.song_title = title
        self.genius_views = genius_views

    def __repr__(self):
        return f"{self.song_title}: {self.genius_views}"
    


def main():
    genius_songs = []

    result = genius.artist_songs(WEEZER_GENIUS_ID, sort="popularity", per_page=50)

    while result["next_page"] is not None:
        next_page = result["next_page"]
        songs = result['songs']
        for item in songs:
            if "stats" in item and "pageviews" in item["stats"]:
                song = GeniusSong(item["full_title"].replace(" by\xa0Weezer", ""), item["stats"]["pageviews"])
            # print(song)
                genius_songs.append(song)
        result = genius.artist_songs(WEEZER_GENIUS_ID, sort="popularity", per_page=50, page=next_page)

    sheet = gspreader.get_sheet("Weezer Data", "all")
    sheet_data = sheet.get_all_records()
    new_data = [ vars(x) for x in genius_songs ]
    print(new_data)

    sheet_data = gspreader.update_sheet_data_by_matching_key(sheet_data, new_data, "song_title")
    gspreader.update_range(sheet, sheet_data)

    return "Success!"



if __name__ == "__main__":
    main()
    

