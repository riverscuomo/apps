import lyricsgenius
import re
from rich import print

import os
from dotenv import load_dotenv
from gspreader import *
from crawlers.core import __main__ as crawlers

load_dotenv()


GENIUS_CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
GENIUS_SECRET = os.getenv("GENIUS_SECRET")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
WEEZER_GENIUS_ID = '12925'

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
# artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title", include_features=True)
# artist = genius.search_songs("Say It Ain't So",  )
# song = artist.songs[0]
# print(vars(song))

# exit()

class GeniusSong:
    def __init__(self, title, genius_views):
        self.song_title = title
        self.genius_views = genius_views

    def __repr__(self):
        return f"{self.song_title}: {self.genius_views}"
    


genius_songs = []

# artist = genius.search_artist("Weezer", sort="title", include_features=True, get_full_info=True, max_songs=1) 
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

# print(artist.id)
# print(songs)


print(genius_songs)

sheet = gspreader.get_sheet("Weezer Data", "all")
sheet_data = sheet.get_all_records()
new_data = [ vars(x) for x in genius_songs ]
print(new_data)

sheet_data = crawlers.update_sheet_data(sheet_data, new_data, "song_title")
update_range(sheet, sheet_data)
    

