import os
import shutil
import re
import datetime
from rich import print

# set the path to the folder you want to move files from
path = f'{os.environ.get("DROPBOX_HOME")}\Weezer Playback Project'

# set the path to the folder you want to move files to
dest = f'{path}\Previous'
''
# set the regex pattern to match the version number in the filename if it exists
# this pattern will match a version number in the format of 1.0.0
# but not match with dates in the format of 2023-01-01
version_pattern = re.compile(r'(\d+\.\d+(?:\.\d+)?)')
#     if only_starts_with:

#         files_to_move = [file for file in ableton_files IF file.lower().startswith(name.lower())]
#     else:
# , only_starts_with=False


def move_named_files(names: list[str]):
    """
    This function moves all files matching a specific name in their filenames 
    from a specified directory to a 'previous' subdirectory.

    Parameters:
    name (str): The name to look for in the filenames.
    """

    names = [name.lower() for name in names]

    # get a list of files in the path
    files = os.listdir(path)


    # loop through the files
    for file in files:

        if file.lower() in names:
            # move the file to the 'previous' subfolder
            shutil.move(os.path.join(path, file), os.path.join(dest, file))

            # print a message to the console
            print(f'Moved "{file}" to Previous')

def move_named_als_files(names: list[str], num_keep: int):
    print(f"\n--- Starting move_named_als_files() with names {names} and num_keep {num_keep} ---")
    names = [name.lower() for name in names]
    
    files = os.listdir(path)
    print(f"All files in directory: {files}")
    
    # Filter files that match the given names and end with .als
    matching_files = [file for file in files if file.endswith('.als') and any(name in file.lower() for name in names)]
    print(f"Files matching names: {matching_files}")
    
    # Sort files by modification time (most recent first)
    matching_files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
    print(f"Sorted matching files: {matching_files}")
    
    # Select files to move (all but the num_keep most recent)
    files_to_move = matching_files[num_keep:]
    print(f"Files to move: {files_to_move}")
    
    for file in files_to_move:
        try:
            shutil.move(os.path.join(path, file), os.path.join(dest, file))
            print(f'Moved "{file}" to Previous')
        except Exception as e:
            print(f'Error moving "{file}": {e}')
    
    if not files_to_move:
        print(f"No files to move (found {len(matching_files)} files, keeping {num_keep})")
            


def move_old_als_files():
    print("\n--- Starting move_old_als_files() ---")
    files = os.listdir(path)
    print(f"All files in directory: {files}")
    
    als_files = [file for file in files if file.endswith('.als') and version_pattern.search(file)]
    print(f"ALS files with version numbers: {als_files}")
    
    filtered_files = [
        file for file in als_files
        if 'scott' not in file.lower() and 'brian' not in file.lower()
    ]
    print(f"Filtered ALS files: {filtered_files}")
    
    filtered_files.sort(key=version_key, reverse=True)
    print(f"Sorted filtered ALS files: {filtered_files}")
    
    if len(filtered_files) > 3:
        files_to_move = filtered_files[3:]
        print(f"Files to move: {files_to_move}")
        
        for file in files_to_move:
            try:
                shutil.move(os.path.join(path, file), os.path.join(dest, file))
                print(f'Moved "{file}" to Previous')
            except Exception as e:
                print(f'Error moving "{file}": {e}')
    else:
        print("No files to move (3 or fewer files found)")

def move_old_json_files():
    print("\n--- Starting move_old_json_files() ---")
    # This pattern will match both YYYY-MM-DD and YYYY-MM formats
    date_pattern = re.compile(r'(\d{4}-\d{2}(?:-\d{2})?)')
    
    files = os.listdir(path)
    print(f"All files in directory: {files}")
    
    json_files = [file for file in files if file.endswith('.json') and date_pattern.findall(file)]
    print(f"JSON files with dates: {json_files}")
    
    # Sort JSON files by modification time (most recent first)
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
    print(f"Sorted JSON files: {json_files}")
    
    # Keep only the 3 newest JSON files
    if len(json_files) > 3:
        files_to_move = json_files[3:]
        print(f"Files to move: {files_to_move}")
        
        for file in files_to_move:
            try:
                shutil.move(os.path.join(path, file), os.path.join(dest, file))
                print(f'Moved "{file}" to Previous')
            except Exception as e:
                print(f'Error moving "{file}": {e}')
    else:
        print("No files to move (3 or fewer JSON files found)")


# Parse version number and convert to tuple (1,0,0) for correct sorting
def version_key(filename):
    version_match = version_pattern.search(filename)
    if version_match:
        version_str = version_match.group(1)
        parts = version_str.split('.')
        # Pad with zeros if there's no patch number
        while len(parts) < 3:
            parts.append('0')
        return tuple(map(int, parts))  # Convert to tuple of ints
    return (0, 0, 0)  # Default version if none is found

def main(subscript_args):
    # Use subscript_args as needed
    print(f"weezerplayback.py main() received arguments: {subscript_args}")
    print(f"Source path: {path}")
    print(f"Destination path: {dest}")
    print(f"Does source path exist? {os.path.exists(path)}")
    print(f"Does destination path exist? {os.path.exists(dest)}")
    
    try:
        move_old_als_files()
        move_old_json_files()
        move_named_als_files(['ss', 'scott', 'shriner'], 2)
        move_named_files(['exportLocatorIds'])
        print("All operations completed successfully")
        return "Success!"
    except Exception as e:
        print(f"An error occurred in main: {e}")
        return str(e)

if __name__ == '__main__':
    main([])










