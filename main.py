import re
import os
import argparse
import inflect
from datetime import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv
import pytz
import importlib.util
import sys
from contextlib import contextmanager

# Load environment variables
load_dotenv(override=True)

# Initialize inflect engine
engine = inflect.engine()

# Constants
AOC_URL = "https://adventofcode.com/2024/day/{}/input"
MAIN_PATH_TEMPLATE = "{}\\solutions\\%s"
SESSION_VAR_NAME = "AOC_SESSION"
DAY_PATTERN = r"\d+-day-.*"

def input_data_exists(day, main_path):
    """Check if input data file exists and is not empty."""
    day_words = engine.number_to_words(day)
    data_path = Path(main_path % f"{day}-day-{day_words}") / "data"
    return data_path.exists() and data_path.stat().st_size > 0

def download_input_if_needed(day, session_token, main_path):
    """Download input data if it does not exist or is empty."""
    day_words = engine.number_to_words(day)
    data_path = Path(main_path % f"{day}-day-{day_words}") / "data"

    if input_data_exists(day, main_path):
        print(f"Input data for Day {day} already exists and is not empty.")
        return

    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(AOC_URL.format(day), headers=headers)

    if response.ok:
        input_data = response.text
        data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(data_path, "w") as f:
            f.write(input_data)
        print(f"Input for Day {day} downloaded.")
    else:
        print(
            f"Failed to download input for Day {day}. Status Code: {response.status_code}"
        )

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Advent of Code CLI.")
    parser.add_argument(
        "--download", 
        action="store_true", 
        help="Download input data"
    )
    parser.add_argument(
        "--day",
        type=int,
        help="Specify a day (defaults to current day in December)"
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run solution for the specified or current day"
    )
    parser.add_argument(
        "--from",
        dest="from_day",
        type=int,
        help="Specify starting day to run solutions (inclusive)"
    )
    parser.add_argument(
        "--to",
        dest="to_day",
        type=int,
        help="Specify ending day to run solutions (inclusive)"
    )
    parser.add_argument(
        "--token",
        type=str,
        help="Advent of Code session token required for downloading input",
    )

    return parser.parse_args()

def get_folders(main_path):
    """Retrieve valid folders for AOC solutions."""
    return list(
        dict(
            sorted(
                {
                    folder_name: int(folder_name.split("-")[0])
                    for folder_name in os.listdir(main_path % "")
                    if re.match(DAY_PATTERN, folder_name)
                }.items(),
                key=lambda x: x[1],
            )
        ).keys()
    )

@contextmanager
def change_directory(directory):
    """Context manager for changing the current working directory."""
    current_directory = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(current_directory)

def run_solution(day_to_process, main_path):
    """Run the solution for a specific day."""
    folders = get_folders(main_path)
    day_folder = next(
        (f for f in folders if int(f.split("-")[0]) == day_to_process), 
        None
    )

    if not day_folder:
        print(f"No solution folder found for day {day_to_process}")
        return

    banner = re.sub(r"[^A-Z ]", "", day_folder.replace("-", " ").upper()).strip()
    print(f"{banner:=^35s}")

    # Construct the path to the solution Python file
    solution_file_name = f"{day_folder}.py"
    solution_folder_path = Path(main_path % day_folder)
    solution_path = solution_folder_path / solution_file_name

    if not solution_path.exists():
        print(f"Solution file {solution_file_name} does not exist in {day_folder}")
        return

    # Import and run the solve function with a temporary directory change
    with change_directory(solution_folder_path):
        spec = importlib.util.spec_from_file_location(day_folder, solution_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        if hasattr(module, "solve"):
            module.solve()
        else:
            print(f"No 'solve' function found in {solution_file_name}")

def adjusted_aoc_day_now():
    '''Calculate the current AOC day accounting for early release timezone offset.'''
    cst = pytz.timezone('America/Chicago')
    now = datetime.now(cst)
    
    # Advent of Code releases puzzles at 00:00 UTC, which is 6:00 PM CST the previous day
    # We need to shift by 5 hours more because we're considering 11:00 PM CST
    if now.hour >= 23:
        # If the current time is on or after 11 PM CST, consider it the following day
        return now.day + 1
    return now.day

def main():
    args = parse_args()
    main_path = os.path.join(os.getcwd(), "solutions", "%s")
    
    # Adjust AOC day handling
    current_day = adjusted_aoc_day_now()

    # Determine the day range to process
    if args.day:
        day_to_process = [args.day]
    else:
        if args.from_day:
            start_day = args.from_day
            end_day = args.to_day if args.to_day else (current_day if datetime.now().month == 12 else None)
        elif args.to_day:
            start_day = current_day if datetime.now().month == 12 else None
            end_day = args.to_day
        else:
            start_day = current_day if datetime.now().month == 12 else None
            end_day = start_day

        if start_day is None or end_day is None:
            print("Please specify a day with --day, --from, or --to, or run during December")
            return

        day_to_process = range(start_day, end_day + 1)

    # Download input if requested
    if args.download:
        session_token = os.getenv(SESSION_VAR_NAME) or args.token
        if not session_token:
            raise ValueError(
                f"Session token is required. Use --token option or store it in the .env file under {SESSION_VAR_NAME}."
            )
        for day in day_to_process:
            download_input_if_needed(day, session_token, main_path)

    # Run solutions if requested
    if args.run:
        for day in day_to_process:
            run_solution(day, main_path)

if __name__ == "__main__":
    main()