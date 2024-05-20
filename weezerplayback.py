import os
import shutil
import re
import datetime
from rich import print

# set the path to the folder you want to move files from
path = f'{os.environ.get("DROPBOX_HOME")}\Weezer Playback Project'

# set the path to the folder you want to move files to
dest = f'{path}\Previous'

# set the regex pattern to match the version number in the filename if it exists
# this pattern will match a version number in the format of 1.0.0
# but not match with dates in the format of 2023-01-01
version_pattern = re.compile(r'(\d+\.\d+\.\d+)')
#     if only_starts_with:

#         files_to_move = [file for file in ableton_files IF file.lower().startswith(name.lower())]
#     else:
# , only_starts_with=False
def move_named_als_files(names: list[str], num_keep: int):
    """
    This function moves all .als files containing a specific name in their filenames 
    from a specified directory to a 'previous' subdirectory, keeping only the 
    num_keep most recent files in the source directory.

    Parameters:
    name (str): The name to look for in the filenames.
    num_keep (int): The number of most recent files to keep in the source directory.
    """
    # get a list of files in the path
    files = os.listdir(path)

    # get the files that have .als extension
    ableton_files = [file for file in files if file.endswith('.als')]

    # get the files that have any of the specified names in the filename
    files_to_move = [file for file in ableton_files if any(name.lower() in file.lower() for name in names)]

    # sort the files by their modification time, descending (most recent first)
    files_to_move.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)

    print(f"All files: {files}")

    # get the files that need to be moved (als files with the specified names)
    files_to_move = files_to_move[num_keep:]

    print(f"Files to move: {files_to_move}")

    # loop through the files
    for file in files_to_move:
        # move the file to the 'previous' subfolder
        shutil.move(os.path.join(path, file), os.path.join(dest, file))

        # print a message to the console
        print(f'Moved "{file}" to Previous')

def move_old_als_files():
    """

    This function moves .als files that have a version number (in the format of 1.0.0) in their names but do not include 'scott' or 'brian', from a specified directory to a 'previous' subdirectory. Additionally, the files are sorted by their version numbers in descending order. If more than three such files are present, all except the first three files are moved to the 'previous' subfolder.

    The function performs the following steps:
    1. Sets a regex pattern to match the version number within the filename.
    2. Obtains a list of all files in the specified directory.
    3. Filters the .als files that have a version number in their name.
    4. Further filters out files if 'scott' or 'brian' (case insensitive) is present in their names.
    5. Sorts the remaining files based on their version numbers, in descending order. 
    6. Moves all but the first three files to the 'previous' subfolder, in case more than three such files are present.

    The directories 'path' and 'dest' (for source and destination directories respectively) need to be set before calling this function. Note that this function does not return any value, but prints the list of files and updates regarding the file movements on the console.

    
    """
    

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

    

    # Sort the files by version number, descending
    files.sort(key=version_key, reverse=True)

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
# Parse version number and convert to tuple (1,0,0) for correct sorting
def version_key(filename):
    version_match = version_pattern.search(filename)
    if version_match:
        version_str = version_match.group(1)
        return tuple(map(int, version_str.split('.')))  # Convert to tuple of ints
    return (0, 0, 0)  # Default version if none is found

def main():

    move_old_als_files()

    move_old_json_files()

    move_named_als_files(['scott', 'shriner', 'ss '], 2)

    return "Success!"
    

if __name__ == '__main__':
    main()










