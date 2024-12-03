import re
import os
import argparse
import inflect
from datetime import datetime
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Initialize inflect engine
engine = inflect.engine()

# Constants
AOC_URL = "https://adventofcode.com/2024/day/{}/input"
MAIN_PATH_TEMPLATE = "{}\\%s"
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
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create the parser for the "run" command
    run_parser = subparsers.add_parser("run", help="Run Advent of Code problems")
    run_parser.add_argument("--all", action="store_true", help="Run all problems")
    run_parser.add_argument(
        "--up-to-today",
        action="store_true",
        help="Run all problems up to and including the current day",
    )
    run_parser.add_argument(
        "--day", 
        type=int, 
        help="Specify a specific day to run"
    )

    # Global options
    parser.add_argument(
        "--download", action="store_true", help="Download today's input"
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

def main():
    args = parse_args()
    main_path = os.getcwd() + "\\%s"
    current_date = datetime.now()

    # Download input if requested and valid
    if args.download and current_date.month == 12:
        session_token = os.getenv(SESSION_VAR_NAME) or args.token
        if not session_token:
            raise ValueError(
                f"Session token is required. Use --token option or store it in the .env file under {SESSION_VAR_NAME}."
            )
        download_input_if_needed(current_date.day, session_token, main_path)
    elif args.download:
        print("It's not December; input download is typically for December only.")

    # Run solutions if "run" command is selected
    if args.command == "run":
        folders = get_folders(main_path)
        if args.day:
            folders = [f for f in folders if int(f.split("-")[0]) == args.day]
        elif not args.all and current_date.month == 12:
            max_day = current_date.day if args.up_to_today else current_date.day
            folders = [f for f in folders if int(f.split("-")[0]) <= max_day]

        if not folders:
            print(f"No folders found for the specified options.")
            return

        for folder in folders:
            banner = re.sub(r"[^A-Z ]", "", folder.replace("-", " ").upper()).strip()
            print(f"{banner:=^35s}")
            os.chdir(main_path % folder)  # Enter the folder
            module = __import__(folder, fromlist=[folder])  # Import as module
            getattr(module, folder).solve()  # Invoke solve method
            os.chdir(main_path % "")  # Return to main directory
            print()

if __name__ == "__main__":
    main()