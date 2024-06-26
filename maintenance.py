import argparse
import contextlib
import importlib
import os
import sys
import traceback
import gspreader
from rich import print
from maintenance_config import *

maintenance_parser = argparse.ArgumentParser(
    description="Runs many modules in the Apps folder."
)
maintenance_parser.add_argument(
    "-m",
    "--module",
    help="A specific module to run. simply put the name of one of the scripts (without the .py)",
)
maintenance_parser.add_argument(
    "-t",
    "--type",
        help="The type of run: short, long, weekly, or biweekly. for a shortRun only: py maintenance.py -t short ",
    choices=["short", "long", "weekly", "biweekly"],)
args = maintenance_parser.parse_args()
# print('args: ', args)

"""
    Windows Task Scheduler runs all "longrun" programs here at 0:01 every morning.

    weeklyImports is on Monday.

    "shortrun" is when you're running manually.

    When you import, it imports all the code but doesn't run until you call main().
    That's good.

    TL; DR: I recommend using python -m to run a Python file, in order to add the current working directory to sys.path and enable relative imports.

    Definitions
    Script: Python file meant to be run with the command line interface.

    Module: Python file meant to be imported.

    Package: directory containing modules/packages. To run packages, these points may be helpful:

    - don't have an __init__.py file in the top level of the package
    - put `from .__main__ import main` in the __init__.py file of the inner package
    - your main function should be in a file called __main__.py in the inner package
    - all other modules should be in a lower level than the __main__.py file

"""


def add_skip_report(result: list):
    """Add the skip report dictionary."""

    result += [
        build_skip_report(x)
        for x in all_imports
        if x.module_name not in [x["module_name"] for x in result]
    ]

    return result


def build_skip_report(x):
    return {
        "last_run_date": todayString,
        "module_name": x.module_name,
        "description": x.description,
        "message": "Skipped.",
        "platform": x.platform,
    }


def clear_modules_from_sys(package_name, path):
    """Remove all modules that were imported from this package so they don't conflict with future imports."""

    # Remove this path so that it doesn't get in the way of future imports.
    sys.path = [e for e in sys.path if path not in e]

    # Remove all the modules that were imported from this package so they don't conflict
    # with future imports.
    loaded_package_modules = [
        key for key, value in sys.modules.items() if package_name in str(value)
    ]
    for key in loaded_package_modules:
        logging.info(f"deleting {key} from sys.modules")
        del sys.modules[key]


def clear_paths():
    """Remove paths that may conflict with this module import"""
    APPS_HOME = os.environ["APPS_HOME"]

    dead_paths = [
        # "C:\\RC Dropbox\\Rivers Cuomo\\Apps",
        f"{APPS_HOME}",
        f"{APPS_HOME}\\credentials\\\\",
        f"{APPS_HOME}\\catalog",
        f"{APPS_HOME}\\new_albums",
        f"{APPS_HOME}\\demos",
        # ".",
    ]
    for d in dead_paths:
        with contextlib.suppress(Exception):
            sys.path.remove(d)


def consolidate_data(sheet_data, result_data):
    """
    Prep the results data for printing to the sheet. Update the data with any new results.
    """
    data = []

    # First iterate through every row in the sheet.
    for sheet_row in sheet_data:
        # If this row has a new result in the results data, append it to data and continue to the next row of the sheet.
        if result_row := in_data(sheet_row, result_data):
            data.append(result_row)
            continue

        # Otherwise, append the sheet row to data.
        data.append(sheet_row)

    # Once you've gone through all the sheet rows and added any new results, add any results for modules that weren't previously part of the sheet.
    for result_row in result_data:
        if result_row is in_data(result_row, data):
            continue
        data.append(result_row)

    return data


def fix_import_names():
    """Fix module name if I've passed the wrong name to the script argument."""
    module = args.module.lower()

    if ".py" in module:
        print("DONT PUT .PY AT THE END OF THE SCRIPT ARGUMENT YOU WANT TO RUN")
        module = module.replace(".py", "")
    if "sheetransfer" in module:
        print("just fyi, sheettransfer has 2 Ts bro...")
        module = module.replace("sheetransfer", "sheettransfer")
    if module == "sheettransfer":
        print("just fyi, sentiment is sheettransfer25 bro...")
        module = module.replace("sheettransfer", "sheettransfer25")
    elif module == "sentiment":
        print("just fyi, sentiment is sentiment11 bro...")
        module = "sentiment11"
    elif module == "newalbums":
        print("just fyi, newalbums is new_albums idiot...")
        module = "new_albums"
    elif module == "iaqualink":
        print("just fyi, iaqualink is pool idiot...")
        module = "pool"
    elif module == "newmusic":
        print("newmusic doesn't exist anymore! You cahnged it to spotkin")
        exit()


    print("You've made a command line module of", module)

    # Then assign the import tuple as the only memeber of the imports list
    result = [x for x in all_imports if x.module_name.lower() == module]
    print(f"imports={result}")

    return result


def get_modules_to_run():
    """ """
    runs = []

    # If you've specified a module to run, make sure that it's name is correct.
    # Names don't need to be fixed if the modules were set from config because those have no errors.
    # It's just when you're running with a module specified at the command line that they may have errors.
    if args.module is not None:
        imports = fix_import_names()
        runs.append(args.module)

    elif args.type is not None:
        

        # If you've specified that you want to run a certain frequency type, collect those modules
        if args.type == "short":
            # # If you've specified that you want to do a short run
            # if argument in ["s", "short", "shortrun"]:
            imports = [
                x for x in all_imports if x.frequency == RunType.short and not x.skipper
            ]
            runs.append("shortRun")
        elif args.type == "weekly":
            imports = [
                x for x in all_imports if x.frequency == RunType.weekly and not x.skipper
            ]
            runs.append
        elif args.type == "biweekly":
            imports = [
                x for x in all_imports if x.frequency == RunType.biweekly and not x.skipper
            ]
            runs.append("biweeklyImports")

    # If you haven't specficed a frequency type, load the short and long runs to start with
    else:
        imports = [
            x for x in all_imports if x.frequency in [RunType.short, RunType.long]
        ]
        runs.extend(["shortRun", "longRun"])

        # # If it's the first day of the month, also run these weekly 
        # if current_day_of_month in [1, 8, 15, 22]:
        #     imports += [x for x in all_imports if x.frequency == RunType.weekly]
        #     print("doing a shortRun + longRun + weeklyImports: \n")

        # Check if today is Sunday (where Monday is 0 and Sunday is 6)
        if current_day_of_week == 6:  # 6 represents Sunday
            imports += [x for x in all_imports if x.frequency == RunType.weekly]
            runs.append("weeklyImports")

        # Twice a month, on the 1st and 15th, do the biweekly imports
        if current_day_of_month in [1, 15]:
            imports += [x for x in all_imports if x.frequency == RunType.biweekly]
            runs.append("biweeklyImports")

            if current_day_of_month == 1:
                imports += [x for x in all_imports if x.frequency == RunType.monthly]
                runs.append("monthlyImports")

    print(f"RunTypes={runs}")

        # remove imports that you don't need to run these days
    imports = [x for x in imports if not x.skipper]

    return imports


def in_data(row, data):
    return next((x for x in data if x["module_name"] == row["module_name"]), False)


def initialize_import(this_import):
    logging.info(" ")
    logging.info(f"this_import={this_import}")

    module_name = this_import.module_name
    module_path = this_import.module_path
    # # setup_file_name = (this_import.setup_file_name)  # will be None if it's simply a module within Apps
    # path = this_import.path

    # Initialize a new report object for this import
    report = Report(todayString, module_name, this_import.description)

    return module_name, module_path, report


def print_result_to_sheet(result: list):
    """Print the results of all the imports and runs to the log in Google Sheets."""
    # print(result)

    skipped = [x for x in all_imports if x.skipper]

    skipped_result = [
        {
            "last_run_date": "",
            "module_name": s.module_name,
            "message": "Skipped.",
            "description": s.description,
            "platform": s.platform,
        }
        for s in skipped
    ]

    result_dicts = [vars(x) for x in result]
    result_dicts += skipped_result

    client = gspreader.get_client()
    sheet = gspreader.get_sheet("Maintenance", "maintenance", client=client)
    sheet_data = sheet.get_all_records()
    data = consolidate_data(sheet_data, result_dicts)
    gspreader.update_range(sheet, data)


def run_module(report, module_path):
    """Import a script from the current directory (Apps), run its main() function, and return the report."""
    logging.info(f"Running {module_path}...")
    new_module = importlib.import_module(module_path)
    logging.info(f"Successfully imported {module_path}. Now time to run its main()....")
    try:
        r = new_module.main()
        message = str(r)
        print(message)
        report.message = message
        logging.info(message)
    except Exception as e:
        r = f"Failure in {module_path}.main(): <{traceback.format_exc()}>"
        print(r)
        report.message = r
        logging.error(r)
    return report


def run():
    logging.info("==========================================================")
    logging.info("MAINTENANCE.PY")

    imports = get_modules_to_run()
    logging.info(imports)

    result = []

    for this_import in imports:

        # Maybe I have to keep resetting this because the individual modules are changing it?
        logging.basicConfig(
            force=True,
            filename="maintenance_log.txt",
            level=logging.INFO,
            format="%(levelname)s: %(asctime)s %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
        )
        module_name, module_path, report = initialize_import(this_import)

        # clear_modules_from_sys(package_name, path) # this seems to mess up the module imports

        try:
            report = run_module(report, module_path)
        except Exception as e:
            additional_message = ""
            r = f"Failure to import {module_name}. <{e}> + {additional_message}"
            logging.error(r)
            report.message = r

        result.append(report)

    for x in result:
        logging.info(x.message)

    return result


def main():
    # print(f"Running maintenance.py with args {args}")
    result = run()
    print(result)

    print_to_sheet = True

    if print_to_sheet:
        print_result_to_sheet(result)


if __name__ == "__main__":
    main()
