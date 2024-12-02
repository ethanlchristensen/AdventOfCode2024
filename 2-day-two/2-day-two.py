
import re

def load_data(name='data'):
    file = open(name, 'r')
    data = [line.strip() for line in file.readlines()]
    file.close()
    for idx in range(len(data)):
        data[idx] = [int(v) for v in data[idx].split(" ")]
    return data

def is_safe(report: list[int]) -> bool:
        s = sorted(report)
        if s == report or s[::-1] == report:
            for idx in range(len(report) - 1):
                v = abs(report[idx] - report[idx + 1])
                if not (v >= 1 and v <= 3):
                    return False
        else:
            return False
        return True
    
def part_one():
    """
    code to solve part one
    """
    reports = load_data()
    safe = 0
    for report in reports:
        if is_safe(report): safe += 1
    return safe

def part_two():
    """
    code to solve part two
    """
    reports = load_data()
    safe = 0
    for report in reports:
        if is_safe(report): safe += 1
        else:
            for idx in range(len(report)):
                new_report = [v for i, v in enumerate(report) if i != idx]
                if is_safe(new_report):
                    safe += 1
                    break
    return safe
    
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
