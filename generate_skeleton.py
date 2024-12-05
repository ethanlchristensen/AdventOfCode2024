import re
import os
import inflect

engine = inflect.engine()

def load_template():
    return """import re

def load_data(name='data'):
    with open(name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def part_one():
    \"\"\"Code to solve part one\"\"\"
    return None

def part_two(): 
    \"\"\"Code to solve part two\"\"\"
    return None

def solve():
    \"\"\"Run solutions for part one and two\"\"\"
    part_one_answer = part_one()
    part_two_answer = part_two()
    
    if part_one_answer:
        print(f"part one: {part_one_answer}")
    if part_two_answer:
        print(f"part two: {part_two_answer}")

if __name__ == '__main__':
    solve()"""

def create_solution_folders():
    os.makedirs("solutions")
    folders = [f for f in os.listdir() if re.search(r'\d+-day-.*', f)]
    to_ignore = len(folders)
    current_folder = os.getcwd()

    for idx in range(1, 26):
        if idx > to_ignore:
            folder_name = f'{idx}-day-{engine.number_to_words(idx)}'
            os.mkdir(f"solutions/{folder_name}")
            os.chdir(f"solutions/{folder_name}")
            
            with open(f'{folder_name}.py', 'w') as file:
                file.write(load_template())
                
            with open('data', 'w') as file:
                pass
        
            with open('__init__.py', 'w') as file:
                pass
            
            os.chdir(current_folder)

if __name__ == '__main__':
    create_solution_folders()