import os
import re
import math
import time
from collections import deque as queue
from bruhcolor import bruhcolored as bc

def load_data(name='data'):
    with open(name, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]
    
def print_path(s, e, data, path):
    sx, sy = s
    ex, ey = e
    data[sy][sx] = bc("  ", 255, 72).colored
    data[ey][ex] = bc("  ", 255, 196).colored
    for row in data:
        print("".join(row).replace(".", "  ").replace("#", bc("  ", None, 255).colored).replace("A", bc("  ", None, 208).colored).replace("B", bc("  ", None, 125).colored))

    for idx, (x, y) in enumerate(path):
        data[y][x] = bc("  ", None, 27).colored
        # os.system("cls")
        # for row in data:
        #     print("".join(row).replace(".", "  ").replace("#", bc("  ", None, 255).colored).replace("A", bc("  ", None, 208).colored).replace("B", bc("  ", None, 125).colored))
        # print()
        # time.sleep(0.02)
    os.system("cls")
    for row in data:
        print("".join(row).replace(".", "  ").replace("#", bc("  ", None, 255).colored).replace("A", bc("  ", None, 208).colored).replace("B", bc("  ", None, 125).colored))
    print()

def part_one():
    """Code to solve part one"""
    start = time.time()

    data = load_data()

    total = 0

    sx, sy = -1, -1
    ex, ey = -1, -1
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "S":
                sx, sy = x, y
            if data[y][x] == "E":
                ex, ey = x, y
    
    def bfs(board, sx, sy):
        seen = set()
        q = queue()
        q.append((sx, sy, [(sx, sy)]))

        while len(q) > 0:
            x, y, p = q.popleft()
            if x == ex and y == ey:
                return p
            for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(data[0]) and 0 <= ny < len(data) and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    if board[ny][nx] in ".EAB":
                        if board[ny][nx] == "B":
                            if board[y][x] != ".":
                                continue
                        if board[ny][nx] == "B":
                            if board[y][x] != "A":
                                continue
                        q.append((nx, ny, p + [(nx, ny)]))

    path = bfs(data, sx, sy)
    base_picoseconds = len(path)
    saved_picosecond_hits = {}

    for y in range(len(data) - 1):
        for x in range(len(data[0]) - 1):
            c1 = (x, y)
            c2 = (x, y + 1)
            nb = [[data[y][x] for x in range(len(data[0]))] for y in range(len(data))]
            nb[c1[1]][c1[0]] = "A"
            nb[c2[1]][c2[0]] = "B"
            path = bfs(nb, sx, sy)
            if path and len(path) < base_picoseconds:
                difference = base_picoseconds - len(path)
                if difference in saved_picosecond_hits:
                    saved_picosecond_hits[difference] += 1
                else:
                    saved_picosecond_hits[difference] = 1

    for y in range(len(data) - 1):
        for x in range(len(data[0]) - 1):
            c1 = (x, y)
            c2 = (x + 1, y)
            nb = [[data[y][x] for x in range(len(data[0]))] for y in range(len(data))]
            nb[c1[1]][c1[0]] = "A"
            nb[c2[1]][c2[0]] = "B"
            path = bfs(nb, sx, sy)
            if path and len(path) < base_picoseconds:
                difference = base_picoseconds - len(path)
                if difference in saved_picosecond_hits:
                    saved_picosecond_hits[difference] += 1
                else:
                    saved_picosecond_hits[difference] = 1   
    
    for k, v in saved_picosecond_hits.items():
        if k > 99:
            total += v

    end = time.time()
    return total, end - start

def part_two(): 
    """Code to solve part two"""
    start = time.time()

    end = time.time()
    return None, end - start

def solve():
    """Run solutions for part one and two"""
    part_one_answer, part_one_time_to_complete = part_one()

    if part_one_answer:
        print(f"part one: {part_one_answer}\npart one time: {part_one_time_to_complete:.4f}s")

    part_two_answer, part_two_time_to_complete = part_two()
    
    if part_two_answer:
        print(f"part two: {part_two_answer}\npart two time: {part_two_time_to_complete:.4f}s")

if __name__ == '__main__':
    solve()
