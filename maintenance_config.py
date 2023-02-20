from datetime import datetime
import logging
import enum
import os

today = datetime.now()
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


chromedriver_warning = """\\nnThis will fail when the chrome version has passed the chromedriver version. Youll have to download the new chromedriver.
            "Download from here https://chromedriver.chromium.org/downloads and replace files in /apps . 
            If theyve updated their terms&conditions and you need to check the box, this program will also fail."""

all_imports = [

    Import(
        module_name="ankimove",
        description="move lyric cards in and out of LYRICS. DOES NOT CREATE CARDS which is done by catalog.py\n\nTo simply create new cards that already have rows in ANKI CARDS FOR LYRICS spreadsheet: uncomment the main() function in catalog/anki_functions.",
        frequency=RunType.short,
        # skipper=True,
        failure_message="\nFREQUENT FAILURE: If there is a new version of anki asking to be downloaded, ankimove.py will fail.\nIf I can't find cards, remember the cards must be created in catalog.py first.",
    ),
    Import(
        module_name="catalog",
        description="Not normally run in maintenance.\nMany functions, including creating rehearsal chart like this https://docs.google.com/spreadsheets/d/1S2dg39D1UAXNfjjR3XogZ8hZ3srXTNuuivHISaFC5dA/edit#gid=268888478",
        frequency=RunType.short,
        skipper=True,
    ),
    Import(
        module_name="demos",
        module_path="demos.__main__",
        description="Performs demo maintenance on dbox/demos and dbox/music-me/bundles. See also these 2 bat scripts that have their own tasks in task scheduler: \nPrivate Update (for uploading the SZNZ data to firestore for your Private app)\nWeezify Update (for uploading the bundles data to Firestore for Weezify) ",
        frequency=RunType.short,
        failure_message="if ffmpeg is not installed on the computer, this will crash maintenance",
        skipper=False,  # This SHOULD be run in maintenance, not its own script??

    ),
    Import(
        module_name="kyoko",
        module_path="kyoko.__main__",
        description="Sends an email to Kyoko if there is a stress level > 0 or a flight duration",
        frequency=RunType.short,
        # skipper=True,
    ),
    Import(
        module_name="lyrictransfer",
        description="copy selected lines from LINE MUNCHER and lyrics/PERSONAL into THE LYRICS SHEET",
        frequency=RunType.short,
        skipper=True,
    ),
    Import(
        module_name="lastfmcrawler",
        module_path="crawlers.lastfmcrawler.__main__",
        description="updates the lastfm data on the all tab in the WEEZER DATA workbook. crawler. scraper.",
        frequency=RunType.short,
        # skipper=True,
        failure_message=chromedriver_warning,
    ),
    Import(
        module_name="new_albums",
        module_path="new_albums.__main__",
        description="Makes a spotify playlist of any albums released this week (filtered by your criteria). if your spotify cred needs to be authorized, the whole program will stop here. It may be the case if chrome is logged into a different spotify, the program will pause here.",
        frequency=RunType.short,
    ),
    
    Import(
        module_name="songdata",
        description="Update the data in the ENCYCLOPEDIA and the SETLIST workbooks.",
        frequency=RunType.weekly,
        failure_message=chromedriver_warning,
    ),
    Import(
        module_name="sheettransfer25",
        description="Analyzes stresses and word_freq for LYRICS and TITLES",
        frequency=RunType.long,
        skipper=True,
    ),
    Import(
        module_name="rhymes",
        description="determines rhymes for LYRICS and TITLES",
        frequency=RunType.long,
        skipper=True,
    ),
    Import(
        module_name="setlistfm",
        description="updates the history tab on in the SETLIST workbook. How many times we've played each song in each market. Fetches data from the setlistfm.com API.",
        frequency=RunType.weekly,
        # skipper=True,
    ),
    Import(
        module_name="geniusweezer",
        description="updates WEEZER DATA. How many times each lyric has been viewed. Fetches data from the genius.com API.",
        frequency=RunType.weekly,
        # skipper=True,
    ),
    
    Import(
        module_name="songpopularity",
        description="""update Spotify stats on the popularity tab in the SETLIST workbook. updates the data for existing rows in SETLIST/popularity tab"
            This is a sheet which tracks the change in popularity over time
            of songs you've chosen to track by adding to this sheet.
            Songs are not added automatically.""",
        frequency=RunType.weekly,
    ),
    Import(
        module_name="spotifycrawler",
        module_path="crawlers.spotifycrawler.__main__",
        description="updates the spotify data on the spotify tab in the SETLIST workbook. crawler. scraper. AND Weezer Data spreadsheet, all tab.",
        frequency=RunType.weekly,
        failure_message=chromedriver_warning,
    ),
    Import(
        module_name="sentiment11",
        description="anyalyzes sentiment for LYRICS and TITLES",
        frequency=RunType.long,
        skipper=True,
    ),
    Import(
        module_name="wme",
        module_path="crawlers.wme.__main__",
        description="""scrape show info from wme webservice and paste it into the calendar. 
        and download the deal sheet pdfs.""",
        frequency=RunType.short,
        # skipper=True,
        failure_message=chromedriver_warning,
    ),
    
    Import(
        module_name="wmepdf",
        description="scrape the downloaded deal sheets and print the data to the Weezer calendar",
        frequency=RunType.long,
        skipper=True,
    ),
    Import(
        module_name="ITB",
        description="scrape the deal sheets for foreign shows and pastes the data to the weezer calendar",
        frequency=RunType.long,
        skipper=True,
    ),
    Import(
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
        skipper=True,
    ),
    # Import(
    #     module_name="newmusic",
    #     description="Makes a spotify playlist for you based on your rules. if your spotify cred needs to be authorized, the whole program will stop here. It may be the case if chrome is logged into a different spotify, the program will pause here.",
    #     frequency=RunType.short,
    #     setup_file_name="__main__",
    #     # path=rf"{base_path}",
    # ),
    Import(
        module_name="spotnik",
        module_path="spotnik.__main__",
        description="Makes a spotify playlist for you based on your rules. if your spotify cred needs to be authorized, the whole program will stop here. It may be the case if chrome is logged into a different spotify, the program will pause here.",
        frequency=RunType.short,
    ),
    Import(
        module_name="pool",
        description="""Set the pool_set_temp in iaqua to the temp in the 'pool' column of CALENDAR. 
        Only effective if and when the pool heater is set to turn on.""",
        frequency=RunType.short,
    ),
    Import(
        module_name="tweetDelete",
        description="deletes the latest tweet older than a week every day ",
        frequency=RunType.short,
        skipper=True,
    ),
]


# Import(
#     "demos_previous",
#     "updates many fields in each demo that are marked to 'inherit_from' another specific demo. You have to fill out the inherit_from field manually. DO THESE HAVE THEIR OWN TASK SCHEDULER NOW?",
# frequency=#     RunType.short,
#     skipper=True,
# ),

# googleScriptsApps = [
#     {
#         "date": "",
#         "module_name": "setPrint",
#         "description": """
#            - print setlists to google drive
#            - print setlists to show appointment in calendar
#            - print ableton_ids to txt files in the Ableton project for Weezer shows for Setlist plugin
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Setlist",
#     },
#     {
#         "date": "Every day, 11pm",
#         "module_name": "codesMaintenance",
#         "description": """
#            delete dupes and codeless rows
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Calendar Maintenance",
#     },
#     {
#         "date": "Every 5 minutes",
#         "module_name": "check date column",
#         "description": """
#             Opens an alert dialog if each row's date isn't 1 day ahead of the previous.
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Calendar Maintenance",
#     },
#     {
#         "date": "On demand under the Drivetimes menu",
#         "module_name": "Flight Options",
#         "description": """
#             Copies data (for up to 2 flights for each date) from the flights tab to the relevant calendar tab row. NOTE: this does not copy the data to your Drives calendar. To do that, simply run drivetimes after running this script.
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Calendar Maintenance",
#     },
#     {
#         "date": "Every morning at 4:00am",
#         "module_name": "Email Kyoko Weather",
#         "description": """
#             Emails Kyoko a pool cover warning if chance of precipitation is above 10%
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Calendar Maintenance",
#     },
#     {
#         "date": "Every morning at 4:00am",
#         "module_name": "Email Tour Manager",
#         "description": """
#             drivetimesBorder() ;
#             elevation();
#             maxElevation();
#             processRows(); // stress level
#             splitRowSymbol(); // properly format the cells that have a row splitter --
#             showStatus(); // if there is a 'C' or a 'P' then add the relevant background color.
#             markMissingData() ;
#             spellcheck(); // corrects any spelling errors in the calendar, such as commerical, bilabo. Set in the spellcheck tab.
#             hideColumns();
#             hide_until_today();
#             // withings(); // also has it's own trigger that runs between 7 and 8 am.
#             setFormatting();
#             setFormulas();
#             set_notes_and_links_in_drivetimes();
#             emailTourManager() Emails Thomas if missing data in the next 14 days of drivetimes.
#     """,
#         "message": "",
#         "platform": "Google Apps Script--Calendar Maintenance.nightlyRun()",
#     },
#     {
#         "date": "On demand under the RC menu in Purchases backup spreadsheet",
#         "module_name": "Firestore purchases",
#         "description": """
#             Copies the firestore purchases records to the spreadsheet.
#             There's a also a function to sum the totals for your partners.
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Setlist",
#     },
#     {
#         "date": "Monday 12am",
#         "module_name": "Set List API",
#         "description": """
#             Serve setlist data on an api for the flutter app to populate its setlist survey.
#             Deployed as a webappp
#             """,
#         "message": "",
#         "platform": "Google Apps Script--Setlist",
#     },
#     {
#         "date": "Monday 12am",
#         "module_name": "Song List Public--add ratings",
#         "description": """ DEPRECATED!!! Gets the flutter app demo ratings from firestore and adds them to the SONG LIST PUBLIC spreadsheet.

# DEPRECATED AS demos.py IS NOW STORING THAT DATA
# IN THE DEMO FILE METADATA.

# In the past it was triggered to run every monday morning.
#         """,
#         "message": "",
#         "platform": "Google Apps Script--Song List (Public)",
#     },
#     {
#         "date": "every night",
#         "module_name": "setlistmanager",
#         "description": """ hide boring columns and delete old show columns,
#                             make columns for upcoming shows,
#         """,
#         "message": "",
#         "platform": "Google Apps Script--Setlist",
#     },
#     {
#         "date": "every night",
#         "module_name": "calendar",
#         "description": """color the VenueVerdict column
#                         hide past rows and boring columns
#                         calculate stress level
#                         determine the tz offset from LA
#                         coloring, fontsize, text alignment.
#                         If youre in Asia, this will always be a day behind.
#                         """,
#         "message": "",
#         "platform": "Google Apps Script--Calendar",
#     },
#     {
#         "date": "every night as part of Titles NIGHTLY RUN",
#         "module_name": "moveRejectedTitles",
#         "description": "From TITLES, moves jd rejects to LYRICS or 'rejects' tab THE NIGHT AFTER HE'S RATED THEM, \nWHETHER OR NOT THEY'VE BEEN RATED BY ALL 4 RATERS  \n(Their ratings are kept in their ratings sheets)",
#         "message": "",
#         "platform": "Google Apps Script--Titles",
#     },
#     {
#         "date": "every night",
#         "module_name": "createLyricDocs",
#         "description": "create lyric docs from titles in the TITLES sheet without a link",
#         "message": "",
#         "platform": "Google Apps Script--Titles",
#     },
#     {
#         "date": "every night",
#         "module_name": "colorColumns() in TITLES maintenance",
#         "description": "grey out the empty stress cells",
#         "message": "",
#         "platform": "Google Apps Script--Titles",
#     },
#     {
#         "date": "every night",
#         "module_name": "drivetimes",
#         "description": "",
#         "message": "",
#         "platform": "Google Apps Script--Calendar",
#     },
#     {
#         "date": "every night at 3-4 am",
#         "module_name": "sethyperlinks()  in TITLES maintenance (attached to TITLES sheet)",
#         "description": "sets the hyperlinks in the titles column for all titles with existing docs",
#         "message": "",
#         "platform": "Google Apps Script--Titles",
#     },
#     {
#         "date": "only when you run it",
#         "module_name": "moveDocs()  in TITLES maintenance (attached to TITLES sheet)",
#         "description": "moves docs from one folder to another based on criteria you set. e.g. move lyric docs with a suzy rating of 3",
#         "message": "",
#         "platform": "Google Apps Script--Titles",
#     },
#     {
#         "date": "every night, 5-6am",
#         "module_name": "Format_number_columns() LYRICS maintenance (attached to TITLES sheet)",
#         "description": "Formats syllable count and word freq to numbers or automatic",
#         "message": "",
#         "platform": "Google Apps Script--Lyrics",
#     },
#     {
#         "date": "every night, 5-6am",
#         "module_name": "move_used() LYRICS maintenance (attached to TITLES sheet)",
#         "description": "Moves lines marked with an 'x' in 'xxx' column to the 'x' tab sheet",
#         "message": "",
#         "platform": "Google Apps Script--Lyrics",
#     },
#     {
#         "date": "",
#         "module_name": "quote_source_lyric_reference",
#         "description": "Simply paste the entire album lyrics on the the albumLyrics tab: https://docs.google.com/spreadsheets/d/1TLsqEaSp9KjW07gxcDTtKZUKfBZUE01-UFgCQYqaGWY/edit#gid=211577159 Then run quote_source  Output will be delivered to the terminal. g apps script LYRICS MAINTENANCE / move_used() runs every night to move the used lines but you have to mark the xxx column with an 'x' in lyrics sheet.",
#         "message": "",
#         "platform": "Google Apps Script--Lyrics",
#     },
#     {
#         "date": "runs every 5 seconds",
#         "module_name": "download_mp3s_from_matty_email() in CALENDAR MAINTENANCE project",
#         "description": "GETS THE latest mix from matty's gmails",
#         "message": "",
#         "platform": "Google Apps Script--Calendar",
#     },
#     {
#         "date": "runs every 2 hours",
#         "module_name": "main in Master Lyrics Script in Google Drive",
#         "description": "Triggered (compiles the latest lyrics in a folder into a document. The IDs of the folder and document must be set in the script.) Manual(compiles the lyrics from whatever folder the Master Lyric Script Doc happens to be in https://docs.google.com/document/d/1q2O5Pj5XX-oXH3ZzWjfSefb1NNEpm4GuGhyDBtdgecs/edit).",
#         "message": "",
#         "platform": "Google Apps Script--Calendar",
#     },
# ]
