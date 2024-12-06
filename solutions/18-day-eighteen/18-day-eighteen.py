import os
import re
import math

def load_data(name='data'):
    with open(name, 'r') as file:
        return [line.strip() for line in file.readlines()]

def part_one():
    """Code to solve part one"""
    return None

def part_two(): 
    """Code to solve part two"""
    return None

def solve():
    """Run solutions for part one and two"""
    part_one_answer = part_one()

    if part_one_answer:
        print(f"part one: {part_one_answer}")

    part_two_answer = part_two()
    
    if part_two_answer:
        print(f"part two: {part_two_answer}")

if __name__ == '__main__':
    solve()
