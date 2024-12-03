
import re

def load_data(name='data'):
    file = open(name, 'r')
    data = [line.strip() for line in file.readlines()]
    file.close()
    return data
    
    
def part_one():
    """
    code to solve part one
    """
    total = 0
    data = load_data()
    pattern = r'mul\((\d+),(\d+)\)'
    for line in data:
        matches = re.findall(pattern=pattern, string=line)
        for match in matches:
            total += int(match[0]) * int(match[1])
    return total

def part_two():
    """
    code to solve part two
    """
    active = True
    total = 0
    data = load_data()
    pattern = r'mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)'
    for line in data:
        matches = re.finditer(pattern=pattern, string=line)
        for match in matches:
            match = match.group()
            if match == "do()":
                active = True
            elif match == "don't()":
                active = False
            else:
                if active:
                    match = match.replace("mul(", "").replace(")", "").split(",")
                    total += int(match[0]) * int(match[1])
    return total
    
def solve():
    """
    code to run part one and part two
    """
    part_one_answer = part_one()
    part_two_answer = part_two()
    
    if part_one_answer:
        print(f"part one: {part_one_answer}")
    if part_two_answer:
        print(f"part two: {part_two_answer}")
    
if __name__ == '__main__':
    """
    code to run solve
    """
    solve()
