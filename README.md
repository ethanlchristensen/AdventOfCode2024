# Advent of Code 2024 Solutions

## Setup

- Need to get you AOC token from your browser
- Create .env file with varable `AOC_SESSION` and set it equal to your session token.
- Now you can use the --download flag to download your inputs.

## Usage

Run `gen_solutions.py` to create all the necessary folders and files to work with the `main.py` file.

The `main.py` file is the main file used for invoking the solution files.

The script uses the current day as context on what solution to run. For example, if the date is `December 04, 2024` then the following command can be used to get it's input data.

```bash
>>> python main.py --download
```

_This command will only download the data if the `data` file is empty or does not exist_


Now you can edit the `part_one()` and `part_two()` functions in each `solutions/<#-day-<day>/#-<day>-<number>.py` file to return the solution to each part of the problem.

You can then use the `main.py` file to run your solutions as you solve them.

```bash
>>> python main.py --run
```

Here are some other ways to run
```bash
>>> python main.py --day 22 --run
# This will run the solutions for day 22

>>> python main.py --day 19 --download --run
# This will download your input data for day 19 and then run the solutions

>>> python main.py --from 1 --download --run
# This will download the input data from December 1 up to the current December day, and run all the solutions

>>> python main.py --from 10 --to 15 --download
# This will download the input data for days 10 - 15

>>> python main.py --from 10 --to 15 --download --run
# This will download the input data for days 10 - 15 and run the solutions
```


