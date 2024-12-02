import re
import os
import argparse
from datetime import datetime

# Set up argument parsing
parser = argparse.ArgumentParser(description="Run Advent of Code problems.")
parser.add_argument("--all", action="store_true", help="Run all problems")
args = parser.parse_args()

main_path = os.getcwd() + "\\%s"
current_date = datetime.now()
current_day = current_date.day
current_month = current_date.month

# Valid folder names follow "#-day-#" that contain a py file with the same names
folders = list(dict(sorted({folder_name: int(folder_name.split('-')[0]) for folder_name in os.listdir(
    main_path % '') if re.match(r'\d*\-day\-.*', folder_name)}.items(), key=lambda x: x[1])).keys())

# Determine whether to run only today's problem or all of them
if not args.all and current_month == 12:
    folders = [folder for folder in folders if int(folder.split('-')[0]) == current_day]

for folder in folders:
    print(f"{re.sub(r'[^A-Z ]', '', folder.replace('-', ' ').upper()).strip():=^35s}")
    # Solution file from the folder
    module = __import__(folder, fromlist=[folder])
    # Get the file as module
    day = getattr(module, folder)
    # Change dir to that folder (to access data)
    os.chdir(main_path % folder)
    # Invoke the solve command for the module
    day.solve()
    # Change dir back to the main path
    os.chdir(main_path % '')
    print()