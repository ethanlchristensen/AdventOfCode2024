import os
import re
import math
import time
import uuid


def load_data(name="data"):
    with open(name, "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def find_all_trail_heads(data):
    trail_heads = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "0":
                trail_heads.append((x, y))
    return trail_heads


def part_one():
    """Code to solve part one"""
    start = time.time()

    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    data = load_data()

    total = 0

    tiles_traversed = {}

    erm = [[" " for _ in range(len(data[0]))] for _ in range(len(data))]

    def check_dir(value, x, y, dir, trail_head_id):
        dx, dy = x + dir[0], y + dir[1]
        if 0 <= dy < len(data) and 0 <= dx < len(data[0]):
            if data[dy][dx] != ".":
                if int(data[dy][dx]) == int(value) + 1:
                    if (dx, dy) not in tiles_traversed[trail_head_id]["seen_xy"]:
                        tiles_traversed[trail_head_id]["seen_xy"].append((dx, dy))
                        erm[dy][dx] = data[dy][dx]
                        if data[dy][dx] == "9":
                            tiles_traversed[trail_head_id]["times_hit_9"] += 1
                            return
                        # we found a valid next tile, so now we need to search in all directions
                        new_value = data[dy][dx]

                        # for row in erm:
                        #     print(" ".join(row))
                        # print()
                        # time.sleep(0.05)

                        check_dir(new_value, dx, dy, directions[0], trail_head_id)
                        check_dir(new_value, dx, dy, directions[1], trail_head_id)
                        check_dir(new_value, dx, dy, directions[2], trail_head_id)
                        check_dir(new_value, dx, dy, directions[3], trail_head_id)
    trail_heads = find_all_trail_heads(data=data)

    for trail_head in trail_heads:
        trail_head_id = str(uuid.uuid4())
        erm[trail_head[1]][trail_head[0]] = "0"
        tiles_traversed[trail_head_id] = {"times_hit_9": 0, "seen_xy": []}
        check_dir("0", trail_head[0], trail_head[1], directions[0], trail_head_id)
        check_dir("0", trail_head[0], trail_head[1], directions[1], trail_head_id)
        check_dir("0", trail_head[0], trail_head[1], directions[2], trail_head_id)
        check_dir("0", trail_head[0], trail_head[1], directions[3], trail_head_id)

    # for row in erm:
    #     print(" ".join(row))
    # print()

    for k, v in tiles_traversed.items():
        # print(k, ":", v)
        total += v["times_hit_9"]

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
        print(
            f"part one: {part_one_answer}\npart one time: {part_one_time_to_complete:.4f}s"
        )

    part_two_answer, part_two_time_to_complete = part_two()

    if part_two_answer:
        print(
            f"part two: {part_two_answer}\npart two time: {part_two_time_to_complete:.4f}s"
        )


if __name__ == "__main__":
    solve()
