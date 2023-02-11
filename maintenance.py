# import contextlib
# import pkgutil
# from datetime import datetime
# from maintenance_config import *
# # from maintenance_config_copy import *
# import gspreader
from rich import print
# import os
# import argparse
import traceback
import runpy
import sys
import importlib


# maintenance_parser = argparse.ArgumentParser(
#     description="Runs many modules in the Apps folder.")
# maintenance_parser.add_argument(
#     "-m",
#     "--module",
#     help="A specific module to run. simply put the name of one of the scripts (without the .py)",
# )
# maintenance_parser.add_argument(
#     "-t",
#     "--type",
#     help="The type of run: short, long, weekly. for a shortRun only: py maintenance.py s ",
# )
# args = maintenance_parser.parse_args()

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

    Package: directory containing modules/packages.

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
            key
            for key, value in sys.modules.items()
            if package_name in str(value)
        ]
    for key in loaded_package_modules:
        logging.info(f"deleting {key} from sys.modules")
        del sys.modules[key]


def clear_paths():
    """ Remove paths that may conflict with this module import"""
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
        if result_row := get_matching_result_row(sheet_row, result_data):
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

    if module == "sentiment":
        print("just fyi, sentiment is sentiment11 bro...")
        module = "sentiment11"

    if module == "newalbums":
        print("just fyi, newalbums is new_albums idiot...")
        module = "new_albums"

    if module == "iaqualink":
        print("just fyi, iaqualink is pool idiot...")
        module = "pool"

    print("You've made a command line module of", module)

    # Then assign the import tuple as the only memeber of the imports list
    result = [x for x in all_imports if x.module_name.lower() == module]
    print(f"imports={result}")

    return result


def get_matching_result_row(sheet_row, result_data):
    """
    If this row was run and has a new result, return it.
    """
    return next(
        (
            result_row
            for result_row in result_data
            if result_row["module_name"] == sheet_row["module_name"]
        ),
        False,
    )


def get_modules_to_run():
    """
    
    """
    # print("get_modules_to_run()")

    if args.type == "short":

        # # If you've specified that you want to do a short run
        # if argument in ["s", "short", "shortrun"]:
        imports = [
            x for x in all_imports if x.frequency == RunType.short and x.skipper != True
        ]
        print("doing a short run only: \n")
        # print(shortRun)

    elif args.type == "weekly":
        imports = [
            x
            for x in all_imports
            if x.frequency == RunType.weekly and x.skipper != True
        ]
        print("doing a weekly Imports run only: \n")
        # print(weeklyImports)

    elif args.module is not None:
        imports = fix_import_names()
    
    else:

        imports = [
            x for x in all_imports if x.frequency in [RunType.short, RunType.long]
        ]

        # If it's MONDAY, also run these scripts
        if datetime.now().weekday() == 0:
            imports = all_imports
            print("doing a shortRun + longRun + weeklyImports: \n")
        else:
            print("doing a shortRun + longRun: \n")

        # remove imports that you don't need to run these days
        imports = [x for x in imports if x.skipper != True]

    return imports


def in_data(row, data):
    return next((x for x in data if x["module_name"] == row["module_name"]), False)


def initialize_import(this_import):
    logging.info(" ")
    logging.info(f"this_import={this_import}")

    package_name = this_import.module_name
    setup_file_name = (this_import.setup_file_name)  # will be None if it's simply a module within Apps
    path = this_import.path

    # Initialize a new report object for this import
    report = Report(todayString, package_name, this_import.description)

    return package_name,setup_file_name,path, report


def print_result_to_sheet(result: list):
    """ Print the results of all the imports and runs to the log in Google Sheets."""
    # print(result)

    skipped = [x for x in all_imports if x.skipper == True]

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


def run_apps_module(report, module_name):
    """ Import a script from the current directory (Apps), run its main() function, and return the report."""
    new_module = importlib.import_module(module_name)
    logging.info(f"Successfully imported {module_name}. Now time to run its main()....")
    try:
        r = new_module.main()
        report.message = str(r)
    except Exception as e:
        r = f"Failure in {module_name}.main(): <{e}>"
        report.message = str(r)
    return report


def run_bat_file():
    
    # BAT FILE WORKS FOR DEMOS BUT NO RETURN VALUE
    bat_dir = "C:\RC Dropbox\Rivers Cuomo\Apps\Z-BAT"
    bat_dir = "C:\RC Dropbox\Rivers Cuomo\Apps\demos"


def run_crawler_package(package_name, setup_file_name, report):
    logging.info(f"package_name.setup_file_name={package_name}.{setup_file_name}")
    setup_module = importlib.import_module(
        f"crawlers.{package_name}",
        # package=f"{crawlers}",
    )
    try:
        r = setup_module.main()
    except Exception as e:
        logging.info(f"Failure to run {setup_module}.main():\n{e}")
        r = f"Failure:\n{e}"
    report.message = str(r)    
    return report


def run_modern_way(this_import):
    MODULE_PATH = this_import.path + "\\__init__.py"
    MODULE_NAME = this_import.module_name
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module 
    spec.loader.exec_module(module)
    module.main()


def run_package_but_not_poetry(package_name, setup_file_name, report):
    logging.info(f"package_name.setup_file_name={package_name}.{setup_file_name}")
    setup_module = importlib.import_module(
        f"{package_name}",
        package=f"{package_name}",
    )
    try:
        r = setup_module.main()
    except Exception as e:
        logging.info(f"Failure to run {setup_module}.main():\n{e}")
        r = f"Failure:\n{e}"
    report.message = str(r)    
    return report


def run_poetry_package(package_name, setup_file_name, path, report):
    """ Import and run a package that uses Poetry."""

    logging.info("run_poetry_package")
    logging.info(f"package_name={package_name}")
    logging.info(f"setup_file_name={setup_file_name}")
    setup_module = importlib.import_module(f"{package_name}.{setup_file_name}")
    logging.info(f"Successfully imported setup module {setup_module} from PACKAGE {package_name}. Now time to run its main()....")

    try:
        r = setup_module.main()
    except Exception as e:
        logging.info(f"Failure to run {setup_module}.main():\n{e}")
        r = f"Failure:\n{e}"

    report.message = str(r)

    return report


def run():

    logging.info("==========================================================")
    logging.info("MAINTENANCE.PY")

    imports = get_modules_to_run()
    logging.info(imports)

    result = []

    for this_import in imports:

        package_name, setup_file_name, path, report = initialize_import(this_import)

        # clear_modules_from_sys(package_name, path) # this seems to mess up the module imports

        if package_name in ["new_albums"]:
            # run_poetry_package(package_name, setup_file_name, path, report)

            # setup_module = importlib.import_module("new_albums")
            # run_main(setup_module)

            # setup_module = importlib.import_module("new_albums", package="new_albums")
            # run_main(setup_module)

            # setup_module = importlib.import_module("new_albums.new_albums", package="new_albums.new_albums")  
            # run_main(setup_module)

            r = runpy.run_module("new_albums", run_name="__main__")
            print(r)

                            

        # elif package_name in ["kyoko"]:

        #     os.system(f"py kyoko\setup.py") # WORKS

        #     # run_package_but_not_poetry(package_name, setup_file_name, report) # module 'kyoko' has no attribute 'main'
        #     # run_modern_way(this_import)

        # elif package_name in ["demos"]:
        #     # run_package_but_not_poetry(package_name, setup_file_name, report) # module 'demos' has no attribute 'main'
        #     os.system(f"py demos\demos\__main__.py") # WORKS
        #     # exit()

        # elif package_name in ["spotnik"]:

        #     report = run_poetry_package(package_name, setup_file_name, path, report) 

        # elif setup_file_name is None:
        #     """
        #     This works well for modules in the current directory such as: pool, songpopularity
        #     """
        #     logging.info("importing an apps.module rather than an apps.package.")
        #     module_name = package_name

        #     try:
        #         report = run_apps_module(report, module_name)
        #     except Exception as e:
        #         additional_message = ""
        #         r = f"Failure to import {module_name}. <{e}> + {additional_message}"
        #         report.message = str(r)

        # else:
        #     logging.info("importing an apps.package.")
        #     try:
        #         report = run_poetry_package(package_name, setup_file_name, path, report)

        #     except Exception as e:
        #         e = traceback.format_exc()        
        #         logging.error(f"Failure to import {package_name}:\n{e}")
        #         r = f"Failure to import {package_name}. <{e}>"
        #         report.message = str(r)

        result.append(report)

    for x in result:
        logging.info(x.message)

    return result


def run_main(setup_module):
    """ inspect and run the main() function of a module"""
    print(setup_module)
    print(dir(setup_module))
    try:
        setup_module.main()
    except Exception as e:
        print(e)

    for importer, modname, ispkg in pkgutil.iter_modules(setup_module.__path__):
        print(f"Found submodule {modname} (is a package: {ispkg})")


def main():

    try:
        print("\nOption 1:")
        runpy.run_module("new_albums", run_name="__main__")
    except Exception as e:
        e = traceback.format_exc() 
        print(e)

    try:
        print("\nOption 2:")
        importlib.import_module("new_albums.__main__").main()
    except Exception as e:
        e = traceback.format_exc() 
        print(e)

    try:
        print("\nOption 3:")
        # importlib.import_module("new_albums.__main__").main()
    except Exception as e:
        e = traceback.format_exc() 
        print(e)

    print('\nprint(sys.modules["new_albums"]):')
    print(sys.modules["new_albums"])

    


    # print(f"Running maintenance.py with args {args}")
    # result = run()

    # print_to_sheet = False

    # if print_to_sheet:

    #     print_result_to_sheet(result)


if __name__ == "__main__":
    main()
