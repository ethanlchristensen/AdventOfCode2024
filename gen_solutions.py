import re
import os
import inflect

engine = inflect.engine()

folders = [val for val in os.listdir() if re.search(r'\d+-day-.*', val)]

to_ignore = len(folders)

template = """
import re

def load_data(name='data'):
    file = open(name, 'r')
    data = [line.strip() for line in file.readlines()]
    file.close()
    return data
    
    
def part_one():
    \"\"\"
    code to solve part one
    \"\"\"
    return None

def part_two():
    \"\"\"
    code to solve part two
    \"\"\"
    return None
    
def solve():
    \"\"\"
    code to run part one and part two
    \"\"\"
    part_one_answer = part_one()
    part_two_answer = part_two()
    
    if part_one_answer:
        print(f"part one: {part_one_answer}")
    if part_two_answer:
        print(f"part two: {part_two_answer}")
    
if __name__ == '__main__':
    \"\"\"
    code to run solve
    \"\"\"
    solve()
"""

current_folder = os.getcwd()

for idx in range(1, 26):
    if idx > to_ignore:
        folder_name = f'{idx}-day-{engine.number_to_words(idx)}'
        os.mkdir(folder_name)
        os.chdir(folder_name)
        
        with open(f'{folder_name}.py', 'w') as file:
            file.write(template)
            
        with open('data', 'w') as file:
            pass
        
        os.chdir(current_folder)