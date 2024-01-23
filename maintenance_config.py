from datetime import datetime
import logging
import enum
import os

today = datetime.now()
today_number = today.day
pattern = "%A, %B %d,  %H:%M %p"
pattern = "%B %d, %Y %H:%M %p"
todayString = today.strftime(pattern)
COMPUTERNAME = os.environ["COMPUTERNAME"]
failure_message = "FAILURE!: \n\n"

logging.basicConfig(
    filename="maintenance_log.txt",
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
)

class Report:
    def __init__(
        self,
        last_run_date: str,
        module_name: str,
        description: str,
        message: str = "",
        platform=COMPUTERNAME,
    ):
        self.last_run_date = last_run_date
        self.module_name = module_name
        
        self.description = description
        self.message = message
        self.platform = platform


class RunType(enum.Enum):
    short = 1
    long = 2
    weekly = 3
    biweekly = 4
    monthly = 5


class Import:
    def __init__(
        self,
        module_name: str,        
        description: str,
        frequency: enum,
        module_path: str=None,
        skipper=False,
        date=today,
        platform=COMPUTERNAME,
        failure_message="",
    ):
        self.module_name = module_name
        self.module_path = module_path or module_name
        self.description = description
        self.frequency = frequency
        self.skipper = skipper
        self.date = date
        self.platform = platform
        self.failure_message = failure_message
    def __repr__(self):
        return f"<Import module_name={self.module_name} || module_path={self.module_path} >"


skip_report = {
    "date": todayString,
    "module_name": "",
    "description": "",
    "message": "",
    "platform": COMPUTERNAME,
}


chromedriver_warning = """
Failure: your chrome version has passed the chromedriver version. 
You'll have to download the new chromedriver. 

- First check your chrome version by going to chrome://settings/help. 
- Then download from here https://chromedriver.chromium.org/downloads 
  and replace files in /apps.
"""
            # If they've updated their terms & conditions and you need to check the box, this program will also fail."""


weezerplayback_import = Import(
    module_name="weezerplayback",
    description="clean up the Weezer Playback folder: move old ableton and json setlists to Previous.",
    frequency=RunType.short,
    # skipper=True,
    # failure_message="\nFREQUENT FAILURE: If there is a new version of anki asking to be downloaded, ankimove.py will fail.\nIf I can't find cards, remember the cards must be created in catalog.py first.",
)

ankimove_import = Import(
    module_name="ankimove",
    description="move lyric cards in and out of LYRICS. DOES NOT CREATE CARDS which is done by catalog.py\n\nTo simply create new cards that already have rows in ANKI CARDS FOR LYRICS spreadsheet: uncomment the main() function in catalog/anki_functions.",
    frequency=RunType.short,
    skipper=True,
    failure_message="\nFREQUENT FAILURE: If there is a new version of anki asking to be downloaded, ankimove.py will fail.\nIf I can't find cards, remember the cards must be created in catalog.py first.",
)

catalog_import = Import(
    module_name="catalog",
    description="Not normally run in maintenance.\nMany functions, including creating rehearsal chart like this https://docs.google.com/spreadsheets/d/1S2dg39D1UAXNfjjR3XogZ8hZ3srXTNuuivHISaFC5dA/edit#gid=268888478",
    frequency=RunType.short,
    skipper=True,
)

demos_import = Import(
        module_name="demos",
        module_path="demos.__main__",
        description="Performs demo maintenance on dbox/demos and dbox/music-me/bundles. See also these 2 bat scripts that have their own tasks in task scheduler: \nPrivate Update (for uploading the SZNZ data to firestore for your Private app)\nWeezify Update (for uploading the bundles data to Firestore for Weezify) ",
        frequency=RunType.short,
        failure_message="if ffmpeg is not installed on the computer, this will crash maintenance",
        skipper=False,  # This SHOULD be run in maintenance, not its own script??

    )

kyoko_import = Import(
        module_name="kyoko",
        module_path="kyoko.__main__",
        description="Sends an email to Kyoko if there is a stress level > 0 or a flight duration",
        frequency=RunType.short,
        # skipper=True,
    )

lyricsmanager_import = Import(
    module_name="lyricsmanager",
    description="""calculates your custom stress rules
                        fill in 4321, 321 columns in LYRICS
                        calculates avg column
                        removes duplicate lyrics
                        colors the columns
                        sets the basic filter in the titles sheet
                        (Note: this program wipes out the hyperlinks in TITLES)
                        
        NOTE: NOW THERE IS ALSO A LYRICSMANAGER SCRIPT IN GOOGLE APPS SCRIPT
            attached to the TITLES sheet
            that creates lyric docs from the titles.
            """,
    frequency=RunType.long,
    skipper=False,
)

spotnik_import = Import(
    module_name="spotnik",
    module_path="spotnik.__main__",
    description="Makes a spotify playlist for you based on your rules. if your spotify cred needs to be authorized, the whole program will stop here. It may be the case if chrome is logged into a different spotify, the program will pause here.",
    frequency=RunType.short,
)

pool_import = Import(
    module_name="pool",
    description="""Set the pool_set_temp in iaqua to the temp in the 'pool' column of CALENDAR. 
    Only effective if and when the pool heater is set to turn on.""",
    frequency=RunType.short,
)

tweetDelete_import = Import(
    module_name="tweetDelete",
    description="deletes the latest tweet older than a week every day ",
    frequency=RunType.short,
    skipper=True,

)

lyrictransfer_import =Import(
        module_name="lyrictransfer",
        description="copy selected lines from LINE MUNCHER and lyrics/PERSONAL into THE LYRICS SHEET",
        frequency=RunType.short,
        skipper=True,
    )

lastfmcrawler = Import(
    module_name="lastfmcrawler",
    module_path="crawlers.lastfmcrawler.__main__",
    description="updates the lastfm data on the all tab in the WEEZER DATA workbook. crawler. scraper.",
    frequency=RunType.biweekly,
    # skipper=True,
    failure_message=chromedriver_warning,
)

new_albums_import = Import(
    module_name="new_albums",
    module_path="new_albums.__main__",
    description="Makes a spotify playlist of any albums released this week (filtered by your criteria). if your spotify cred needs to be authorized, the whole program will stop here. It may be the case if chrome is logged into a different spotify, the program will pause here.",
    frequency=RunType.short,
)

songdata_import = Import(
    module_name="songdata",
    description="Update the data in the ENCYCLOPEDIA and the SETLIST workbooks.",
    frequency=RunType.biweekly,
    failure_message=chromedriver_warning,
)

sheettransfer25_import = Import(
    module_name="sheettransfer25",
    description="Analyzes stresses and word_freq for LYRICS and TITLES",
    frequency=RunType.long,
    skipper=False,
)

rhymes_import = Import(
    module_name="rhymes",
    description="determines rhymes for LYRICS and TITLES",
    frequency=RunType.long,
    skipper=False,
)

setlistfm_import = Import(
    module_name="setlistfm",
    description="updates the history tab on in the SETLIST workbook. How many times we've played each song in each market. Fetches data from the setlistfm.com API.",
    frequency=RunType.weekly,
    # skipper=True,
)

geniusweezer_import = Import(
    module_name="geniusweezer",
    description="updates WEEZER DATA. How many times each lyric has been viewed. Fetches data from the genius.com API.",
    frequency=RunType.weekly,
    # skipper=True,
)

songpopularity_import = Import(
    module_name="songpopularity",
    description="""update Spotify stats on the popularity tab in the SETLIST workbook. updates the data for existing rows in SETLIST/popularity tab"
        This is a sheet which tracks the change in popularity over time
        of songs you've chosen to track by adding to this sheet.
        Songs are not added automatically.""",
    frequency=RunType.weekly,
)

spotifycrawler_import = Import(
    module_name="spotifycrawler",
    module_path="crawlers.spotifycrawler.__main__",
    description="updates the spotify data on the spotify tab in the SETLIST workbook. crawler. scraper. AND Weezer Data spreadsheet, all tab.",
    frequency=RunType.weekly,
    failure_message=chromedriver_warning,
    skipper=True,
)

sentiment11_import = Import(
    module_name="sentiment11",
    description="anyalyzes sentiment for LYRICS and TITLES",
    frequency=RunType.long,
    skipper=True,
)

wme_import = Import(
    module_name="wme",
    module_path="crawlers.wme.__main__",
    description="""scrape show info from wme webservice and paste it into the calendar. 
    and download the deal sheet pdfs.""",
    frequency=RunType.short,
    # skipper=True,
    failure_message=chromedriver_warning,
)

wmepdf_import = Import(
    module_name="wmepdf",
    description="scrape the downloaded deal sheets and print the data to the Weezer calendar",
    frequency=RunType.long,
    skipper=True,
)

ITB_import = Import(
    module_name="ITB",
    description="scrape the deal sheets for foreign shows and pastes the data to the weezer calendar",
    frequency=RunType.long,
    skipper=True,
)

lyricsmanager_import = Import(
    module_name="lyricsmanager",
    description="""calculates your custom stress rules
                        fill in 4321, 321 columns in LYRICS
                        calculates avg column
                        removes duplicate lyrics
                        colors the columns
                        sets the basic filter in the titles sheet
                        (Note: this program wipes out the hyperlinks in TITLES)
                        
        NOTE: NOW THERE IS ALSO A LYRICSMANAGER SCRIPT IN GOOGLE APPS SCRIPT
            attached to the TITLES sheet
            that creates lyric docs from the titles.
            """,
    frequency=RunType.long,
    skipper=False,
)

bandsweplaywith_import = Import(
    module_name="bandsweplaywith",
    description="updates the Bands We Play With Spotify playlist from the Other Bands column in the Calendar spreadsheet. Fetches data from the setlist.fm API.",
    frequency=RunType.weekly,
    # skipper=True,
)

all_imports = [

    pool_import,
    new_albums_import,
    spotnik_import,
    kyoko_import,
    weezerplayback_import,
    lyricsmanager_import,
    bandsweplaywith_import,

    demos_import,

    ankimove_import,
    catalog_import, 
    
    tweetDelete_import,
    lyrictransfer_import,
    lastfmcrawler,
    
    songdata_import,
    sheettransfer25_import,
    rhymes_import,
    setlistfm_import,
    geniusweezer_import,
    songpopularity_import,
    spotifycrawler_import,
    sentiment11_import,
    wme_import,
    wmepdf_import,
    ITB_import,

]
