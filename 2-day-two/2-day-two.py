def load_data(name='data'):
    file = open(name, 'r')
    data = [line.strip() for line in file.readlines()]
    file.close()
    for idx in range(len(data)):
        data[idx] = [int(v) for v in data[idx].split(" ")]
    return data

def is_safe(report: list[int]) -> bool:
        return False if not any([report == sorted(report), report == sorted(report)[::-1]]) else all([(abs(report[idx] - report[idx + 1]) >= 1 and abs(report[idx] - report[idx + 1]) <= 3) for idx in range(len(report) - 1)])
    
def part_one():
    """
    code to solve part one
    """
    return sum([1 if (is_safe(report)) else 0 for report in load_data()])

def part_two():
    """
    code to solve part two
    """
    return sum([1 if (is_safe(report) or any([is_safe([v for i, v in enumerate(report) if i != idx]) for idx in range(len(report))])) else 0 for report in load_data()])
    
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
