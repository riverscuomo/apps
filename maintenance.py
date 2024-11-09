import argparse
import enum
import importlib
import traceback
import gspreader
from rich import print
from datetime import datetime
import os
import logging
# Windows Task Scheduler runs all "longrun" programs here at 0:01 every morning.

# weeklyImports is on Monday.

# "shortrun" is when you're running manually.

# When you import, it imports all the code but doesn't run until you call main().
# That's good.

# TL; DR: I recommend using python -m to run a Python file, in order to add the current working directory to sys.path and enable relative imports.

# Definitions
# Script: Python file meant to be run with the command line interface.

# Module: Python file meant to be imported.

# Package: directory containing modules/packages. To run packages, these points may be helpful:

# - don't have an __init__.py file in the top level of the package
# - put `from .__main__ import main` in the __init__.py file of the inner package
# - your main function should be in a file called __main__.py in the inner package
# - all other modules should be in a lower level than the __main__.py file


today = datetime.now()
current_day_of_month = today.day
current_day_of_week = today.weekday()
pattern = "%A, %B %d,  %H:%M %p"
pattern = "%B %d, %Y %H:%M %P"
# patterin in 12 hour time
pattern = "%B %d, %Y %I:%M %p"
todayString = today.strftime(pattern)
COMPUTERNAME = os.environ["COMPUTERNAME"]
failure_message = "FAILURE!: \n\n"

logging.basicConfig(
    filename="maintenance_log.txt",
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
)

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
        
        message: str,
      
        frequency: enum,
          last_run_date: str=None,
        module_path: str=None,
        skipper=False,
        date=today,
        platform=COMPUTERNAME,
        failure_message="",
    ):
        self.module_name = module_name
        self.module_path = module_path or module_name
        self.description = description
        self.last_run_date = last_run_date
        self.message = message
        self.frequency = frequency
        self.skipper = skipper
        self.date = date
        self.platform = platform
        self.failure_message = failure_message
    @classmethod
    def from_dict(cls, data):
        print(data)

        module_name = data["module_name"]
        module_path = data.get("module_path", None)
        last_run_date = data.get("last_run_date", None)
        description = data["description"]
        message = data.get("message", "")
        frequency = RunType[data["frequency"]] if data.get("frequency") else None
        skipper = data["status"].upper() != "TRUE" if "status" in data else False
        date_value = data.get("date", today)
        platform = data.get("platform", COMPUTERNAME)
        failure_message = data.get("failure_message", "")

        return cls(
            module_name=module_name,
            description=description,
            message=message,
            last_run_date=last_run_date,
            frequency=frequency,
            module_path=module_path,
            skipper=skipper,
            date=date_value,
            platform=platform,
            failure_message=failure_message,
        )


    def to_dict(self):
        return {
            "module_name": self.module_name,
            "module_path": self.module_path,
            "description": self.description,
            "last_run_date": self.last_run_date,
            "message": getattr(self, 'message', ''),  # Use getattr to handle if 'message' might not exist
            "frequency": self.frequency.name if self.frequency else None,
            "status": "FALSE" if self.skipper else "TRUE",
            "date": self.date,
            "platform": self.platform,
            "failure_message": self.failure_message,
        }


    def __repr__(self):
        return f"<Import module_name={self.module_name} || module_path={self.module_path} >"




def create_main_parser():
    """ Define the main argument parser """
    parser = argparse.ArgumentParser(
        description="Runs many modules in the Apps folder."
    )
    parser.add_argument(
        "-m", "--module", help="A specific module to run."
    )
    parser.add_argument(
        "-t", "--type", choices=["short", "long", "weekly", "biweekly"],
        help="The type of run: short, long, weekly, or biweekly."
    )
    return parser

def parse_args():
    main_parser = create_main_parser()
    args, remaining_argv = main_parser.parse_known_args()

    if '--' in remaining_argv:
        subscript_position = remaining_argv.index('--')
        subscript_args = remaining_argv[subscript_position + 1:]
        remaining_argv = remaining_argv[:subscript_position]
    else:
        subscript_args = []

    return args, subscript_args



def fix_import_names(all_imports):
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

    if not result:
        print('something wrong, did not find the module you specified in the config')
        exit()
    print(f"imports={result}")

    return result


def get_modules_to_run(all_imports: list[Import]):
    """ """
    runs = []

    # If you've specified a module to run, make sure that it's name is correct.
    # Names don't need to be fixed if the modules were set from config because those have no errors.
    # It's just when you're running with a module specified at the command line that they may have errors.
    if args.module is not None:
        imports = fix_import_names(all_imports)
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


def run_module(this_import: Import, subscript_args: list):
    """Import a script from the current directory (Apps), run its main() function, and return the this_import."""
    this_import.last_run_date = todayString
    this_import.platform = COMPUTERNAME
    module_path = this_import.module_path
    logging.info(f"Running {module_path} with args {subscript_args}...")
    try:
        new_module = importlib.import_module(module_path)
    except Exception as e:
        r = f"Failure to import {module_path}. <{e}>"
        print(r)
        this_import.message = r
        
        logging.error(r)
        return this_import
    try:
        r = new_module.main(subscript_args)  
        message = str(r)
        logging.info(message)
        this_import.message = message
    except Exception as e:
        r = f"Failure in {module_path}.main(): <{traceback.format_exc()}>"
        print(r)
        this_import.message = r
        logging.error(r)
    return this_import

def run(all_imports):
    logging.info("==========================================================")
    logging.info("MAINTENANCE.PY")

    imports = get_modules_to_run(all_imports)

    for this_import in imports:
        logging.basicConfig(
            force=True,
            filename="maintenance_log.txt",
            level=logging.INFO,
            format="%(levelname)s: %(asctime)s %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
        )


        this_import = run_module(this_import, subscript_args)


def main():
    print(f"Running maintenance.py with args {args}")

    sheet = gspreader.get_sheet("Maintenance", "maintenance")

    data = sheet.get_all_records()

    all_imports = [Import.from_dict(x) for x in data]

    run(all_imports)

    data = [x.to_dict() for x in all_imports]

    gspreader.update_range(sheet, data)



args, subscript_args = parse_args()


if __name__ == "__main__":
    main()

