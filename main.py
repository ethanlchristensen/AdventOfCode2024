import re
import os
import argparse
from datetime import datetime

# set up argument parsing
parser = argparse.ArgumentParser(description="Run Advent of Code problems.")
parser.add_argument("--all", action="store_true", help="Run all problems")
args = parser.parse_args()

main_path = os.getcwd() + "\\%s"
current_date = datetime.now()
current_day = current_date.day
current_month = current_date.month

# valid folder names follow "#-day-#" that contain a py file with the same names
folders = list(dict(sorted({folder_name: int(folder_name.split('-')[0]) for folder_name in os.listdir(
    main_path % '') if re.match(r'\d*\-day\-.*', folder_name)}.items(), key=lambda x: x[1])).keys())

# determine whether to run only today's problem or all of them
if not args.all and current_month == 12:
    folders = [folder for folder in folders if int(folder.split('-')[0]) == current_day]

# run the solutions
for folder in folders:
    print(f"{re.sub(r'[^A-Z ]', '', folder.replace('-', ' ').upper()).strip():=^35s}")
    module = __import__(folder, fromlist=[folder])
    day = getattr(module, folder)
    os.chdir(main_path % folder)
    day.solve()
    os.chdir(main_path % '')
    print()