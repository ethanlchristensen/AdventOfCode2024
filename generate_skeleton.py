import re
import os
import inflect

engine = inflect.engine()


def load_template():
    return """import os
import re
import math
import time

def load_data(name='data'):
    with open(name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def part_one():
    \"\"\"Code to solve part one\"\"\"
    start = time.time()

    end = time.time()
    return None, end - start

def part_two(): 
    \"\"\"Code to solve part two\"\"\"
    start = time.time()

    end = time.time()
    return None, end - start

def solve():
    \"\"\"Run solutions for part one and two\"\"\"
    part_one_answer, part_one_time_to_complete = part_one()

    if part_one_answer:
        print(f"part one: {part_one_answer}\\npart one time: {part_one_time_to_complete:.4f}s")

    part_two_answer, part_two_time_to_complete = part_two()
    
    if part_two_answer:
        print(f"part two: {part_two_answer}\\npart two time: {part_two_time_to_complete:.4f}s")

if __name__ == '__main__':
    solve()
"""


def create_solution_folders():
    current_folder = os.getcwd()

    if not os.path.exists(os.path.join(current_folder, "solutions")):
        print(
            f"Creating 'solutions' folder at {os.path.join(current_folder, 'solutions')}"
        )
        os.makedirs(os.path.join(current_folder, "solutions"))

    for idx in range(1, 26):
        folder_name = f"{idx}-day-{engine.number_to_words(idx)}"
        file_name = f"{folder_name}.py"
        folder_path = os.path.join(current_folder, "solutions", folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"Created folder '{folder_name}' at '{folder_path}'")
            os.chdir(folder_path)

            with open(file_name, "w") as file:
                file.write(load_template())
            
            print(f"\tCreated file '{file_name}' at '{folder_path}\\{file_name}' ")

            with open("data", "w") as file:
                pass
            print(f"\tCreated file 'data' at '{folder_path}\\data' ")

            with open("__init__.py", "w") as file:
                pass
            print(f"\tCreated file '__init__.py' at '{folder_path}\\__init__.py' ")

            os.chdir(current_folder)
            
        else:
            print(f"Folder '{folder_name}' already exists at '{folder_path}', skiping . . .")


if __name__ == "__main__":
    create_solution_folders()
