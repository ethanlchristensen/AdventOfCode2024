import os
import re
import math
import time

directions = [
    (0,1),
    (0,-1),
    (1,0),
    (-1,0),
]

def load_data(name='datasmall3', part=1):
    with open(name, 'r') as file:
        lines = file.readlines()
        if part == 2:
            for idx in range(len(lines)-1):
                lines[idx] = lines[idx].replace("#", "##"
                ).replace("O", "[]"
                ).replace(".", ".."
                ).replace("@", "@.")
        data =  [list(line.strip()) for line in lines if line.strip() != ""]
        return data[:-1], data[-1]

def can_push(point, dir, data):
    dx, dy = point[0] + dir[0], point[1] + dir[1]
    if 0 <= dx < len(data[0]) and 0 <= dy < len(data):
        if data[dy][dx] == "#":
            return False
        if data[dy][dx] == "O":
            return can_push((dx, dy), dir, data)
        if data[dy][dx] == ".":
            return True
    return False

def can_move(point, dir, data):
    dx, dy = point[0] + dir[0], point[1] + dir[1]
    if 0 <= dx < len(data[0]) and 0 <= dy < len(data):
        if data[dy][dx] == ".":
            return True
        elif data[dy][dx] == "#":
            return False
        elif data[dy][dx] == "O":
            return can_push(point, dir, data)
    else:
        return False

def get_direction(char: str):
    if char == "^":
        return (0, -1)
    if char == ">":
        return (1, 0)
    if char == "<":
        return (-1, 0)
    if char == "v":
        return (0, 1)

def get_robot_position(data):
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "@":
                return (x, y)

def push_boxes(point, dir, data):
    points = [point]
    current_point = point
    current_point_value = data[point[1]][point[0]]
    while current_point_value != ".":
        current_point = current_point[0] + dir[0], current_point[1] + dir[1]
        current_point_value = data[current_point[1]][current_point[0]]
        points.append(current_point)

    data_copy = data[:]

    for idx in range(len(points) - 1,  0, -1):
        p1 = points[idx]
        p2 = points[idx - 1]
        tmp = data[p1[1]][p1[0]]
        data[p1[1]][p1[0]] = data[p2[1]][p2[0]]
        data[p2[1]][p2[0]] = tmp

    return data

def perfrom_move(point, dir, data):
    dx, dy = point[0] + dir[0], point[1] + dir[1]
    if data[dy][dx] == "O":
        data = push_boxes(point, dir, data)
        return data, (dx, dy)
    elif data[dy][dx] == ".":
        data[dy][dx] = "@"
        data[point[1]][point[0]] = "."
    return data, (dx, dy)

def get_gps_coordinates(data):
    total = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "O":
                total += (100 * y) + x
    return total

def part_one():
    """Code to solve part one"""
    start = time.time()

    data, moves = load_data()

    robot_position = get_robot_position(data)

    for move in moves:
        direction = get_direction(move)
        if can_move(robot_position, direction, data):
            data, robot_position = perfrom_move(robot_position, direction, data)
    
    total = get_gps_coordinates(data)

    end = time.time()
    return total, end - start

def can_push_up_down(point1, point2, dir, data):
    dx1, dy1 = point1[0] + dir[0], point1[1] + dir[1]
    dx2, dy2 = point2[0] + dir[0], point2[1] + dir[1]
    if data[dy1][dx1] == "#" or data[dy2][dx2] == "#":
        return False
    if data[dy1][dx1] == data[point1[1]][point1[0]] and data[dy2][dx2] == data[point2[1]][point2[0]]:
        return can_push_up_down((dx1, dy1), (dx2, dy2), dir, data)
    if data[dy1][dx1] == "." and data[dy2][dx2] == ".":
        return True
    return False

def can_push_left_right(point, dir, data):
    dx, dy = point[0] + dir[0], point[1] + dir[1]
    if data[dy][dx] == "#":
        return False
    if data[dy][dx] in ["[", "]"]:
        return can_push_left_right((dx, dy), dir, data)
    if data[dy][dx] == ".":
        return True
    return False

def can_move_2(point, dir, data):
    dx, dy = point[0] + dir[0], point[1] + dir[1]
    if 0 <= dx < len(data[0]) and 0 <= dy < len(data):
        if data[dy][dx] == ".":
            return True
        elif data[dy][dx] == "#":
            return False
        elif data[dy][dx] in ["[", "]"]:
            if dir in [(0, 1), (0, -1)]:
                p1 = (dx, dy)
                p2 = (dx - 1, dy)
                if data[dy][dx] == "[":
                    p2 = (dx + 1, dy)
                return can_push_up_down(p1, p2, dir, data)
            else:
                return can_push_left_right((dx, dy), dir, data)
    else:
        return False

def get_direction(char: str):
    if char == "^":
        return (0, -1)
    if char == ">":
        return (1, 0)
    if char == "<":
        return (-1, 0)
    if char == "v":
        return (0, 1)

def push_boxes_up_down(point1, dir, data):
    # if dir[1] == 1:
    #     print(f"We are pushing boxes down")
    # else:
    #     print("We are pushing boxes up")
    points = []
    current_point_1 = point1
    current_point_2 = [current_point_1[0], current_point_1[1]]
    if data[point1[1]+dir[1]][point1[0]+dir[0]] == "[":
        current_point_2[0] += 1
    else:
        current_point_2[0] -= 1
    current_point_2 = tuple(current_point_2)
    points.append((current_point_1, current_point_2))
    current_point_1_value = data[point1[1]][point1[0]]
    current_point_2_value = data[point1[1]][point1[0] + (1 if data[point1[1]][point1[0]] == "[" else -1)]
    while True:
        if current_point_1_value == "." and current_point_2_value == ".":
            break
        # print(f"while loop : {points}")
        current_point_1 = current_point_1[0] + dir[0], current_point_1[1] + dir[1]
        current_point_2 = current_point_2[0] + dir[0], current_point_2[1] + dir[1]
        current_point_1_value = data[current_point_2[1]][current_point_2[0]]
        current_point_2_value = data[current_point_2[1]][current_point_2[0]]
        points.append((current_point_1, current_point_2))

    # print(f"Points to swap: {points}")

    for idx in range(len(points) - 1,  1, -1):
        p11, p12 = points[idx]
        p21, p22 = points[idx - 1]

        tmp = data[p11[1]][p11[0]]
        data[p11[1]][p11[0]] = data[p21[1]][p21[0]]
        data[p21[1]][p21[0]] = tmp

        tmp = data[p12[1]][p12[0]]
        data[p12[1]][p12[0]] = data[p22[1]][p22[0]]
        data[p22[1]][p22[0]] = tmp
    
    p1 = points[0][0]
    p2 = (p1[0] + dir[0], p1[1] + dir[1])
    tmp = data[p1[1]][p1[0]]
    data[p1[1]][p1[0]] = data[p2[1]][p2[0]]
    data[p2[1]][p2[0]] = tmp

    return data

def push_boxes_left_right(point, dir, data):
    points = [point]
    current_point = point
    current_point_value = data[point[1]][point[0]]
    while current_point_value != ".":
        current_point = current_point[0] + dir[0], current_point[1] + dir[1]
        current_point_value = data[current_point[1]][current_point[0]]
        points.append(current_point)

    for idx in range(len(points) - 1,  0, -1):
        p1 = points[idx]
        p2 = points[idx - 1]
        tmp = data[p1[1]][p1[0]]
        data[p1[1]][p1[0]] = data[p2[1]][p2[0]]
        data[p2[1]][p2[0]] = tmp

    return data

def perfrom_move_2(point, dir, data):
    dx, dy = point[0] + dir[0], point[1] + dir[1]
    if data[dy][dx] in ["[", "]"]:
        if dir in [(0, 1), (0, -1)]:
            data = push_boxes_up_down(point, dir, data)
        else:
            data = push_boxes_left_right(point, dir, data)
        return data, (dx, dy)
    elif data[dy][dx] == ".":
        data[dy][dx] = "@"
        data[point[1]][point[0]] = "."
    return data, (dx, dy)

def get_gps_coordinates_2(data):
    total = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == "[":
                total += (100 * y) + x
    return total

def part_two(): 
    """Code to solve part two"""
    start = time.time()

    data, moves = load_data(part=2)

    robot_position = get_robot_position(data)

    for move in moves:
        direction = get_direction(move)
        if can_move_2(robot_position, direction, data):
            data, robot_position = perfrom_move_2(robot_position, direction, data)

    total = get_gps_coordinates_2(data)

    for row in data:
        print(" ".join(row))
    print()

    end = time.time()
    return total, end - start

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
