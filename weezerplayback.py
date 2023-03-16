import os
import shutil
import re
import datetime
from rich import print

# set the path to the folder you want to move files from
path = f'{os.environ.get("DROPBOX_HOME")}\Weezer Playback Project'

# set the path to the folder you want to move files to
dest = f'{path}\Previous'


def move_old_als_files():

    # set the regex pattern to match the version number in the filename if it exists
    # this pattern will match a version number in the format of 1.0.0
    # but not match with dates in the format of 2023-01-01
    version_pattern = re.compile(r'(\d+\.\d+\.\d+)')

    # get a list of files in the path
    files = os.listdir(path)

    # filter in the files that have .als extension and have a version number in the filename
    files = [file for file in files if file.endswith('.als') and version_pattern.findall(file)]

    # filter out the files that have 'scott' or 'brian' in the filename
    files = [
        file
        for file in files
        if 'scott' not in file.lower() and 'brian' not in file.lower()
    ]

    # sort the files by version number, descending
    files.sort(key=lambda x: version_pattern.findall(x)[0], reverse=True)

    print(files)

    if len(files) > 3:

        # keep the first two files here but move all the others to the 'previous' subfolder
        files = files[3:]

        # loop through the files
        for file in files:

            # move the file to the 'previous' subfolder
            shutil.move(f'{path}\{file}', f'{dest}\{file}')

            # print a message to the console
            print(f'moved "{file}" to Previous')
            

def move_old_json_files():
    """ Move any json files that have a date in the filename that is in the past to the 'Previous' subfolder"""
    # set the regex pattern to match the date in the filename if it exists
    # this pattern will match a date in the format of 2023-01-01
    # but not match with version numbers in the format of 1.0.0
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')

    # get a list of files in the path
    files = os.listdir(path)

    # filter in the files that have .json extension and have a date in the filename
    files = [file for file in files if file.endswith('.json') and date_pattern.findall(file)]

    # loop through the files
    for file in files:

        # get the date from the filename
        date = date_pattern.findall(file)[0]

        # convert the date string to a datetime object
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        # if the date is at least 1 day in the past
        if date < datetime.datetime.now() - datetime.timedelta(days=1):
        

            # move the file to the 'previous' subfolder
            shutil.move(f'{path}\{file}', f'{dest}\{file}')

            # print a message to the console
            print(f'moved "{file}" to Previous')


def main():

    move_old_als_files()

    move_old_json_files()

    return "Success!"
    

if __name__ == '__main__':
    main()










