import os
import re
import math
import time


def load_data(name="data"):
    with open(name, "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def part_one():
    """Code to solve part one"""
    start = time.time()

    data = load_data()
    datastr = "".join([c for row in data for c in row])

    crops = {crop: datastr.count(crop) for crop in set(datastr)}
    crop_seen_plots = {crop:set() for crop in crops}
    crop_perimeters = {crop:{} for crop in crops}
    crop_region_totals = {crop:{} for crop in crops}
    
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]

    hits = [[" " for _ in range(len(data[0]))] for _ in range(len(data))]

    def check_dir(crop, point, crop_region):
        x, y = point
        if not 0 <= x < len(data[0]) or not 0 <= y < len(data):
            crop_seen_plots[crop].add(point)
            crop_perimeters[crop][crop_region] += 1
            return 0
        if data[y][x] != crop:
            crop_seen_plots[crop].add(point)
            crop_perimeters[crop][crop_region] += 1
            return 0
        if point in crop_seen_plots[crop]:
            crop_seen_plots[crop].add(point)
            return 0

        crop_seen_plots[crop].add(point)

        plot_hits = 0
        for direction in directions:
            plot_hits += check_dir(crop, (x + direction[0], y + direction[1]), crop_region)
        return plot_hits + 1

    for crop, crop_count in crops.items():
        crops_found = 0
        crop_region = 0
        while crops_found != crop_count:
            if crop_region not in crop_seen_plots[crop]:
                crop_perimeters[crop][crop_region] = 0
                crop_region_totals[crop][crop_region] = 0
            region_crops = 0
            crop_start_point = None
            for y in range(len(data)):
                for x in range(len(data[0])):
                    if (x, y) in crop_seen_plots[crop]: continue
                    if data[y][x] == crop:
                        crop_start_point = (x, y)
                        break
                else:
                    continue
                break
            region_crops = check_dir(crop, crop_start_point, crop_region)
            crops_found += region_crops
            crop_region_totals[crop][crop_region] = region_crops
            crop_region += 1
    
    total = 0

    for crop in crop_region_totals:
        region_totals = crop_region_totals[crop]
        region_perimeters = crop_perimeters[crop]
        for region in region_totals:
            total += region_totals[region] * region_perimeters[region]

    end = time.time()
    return total, end - start


def part_two():
    """Code to solve part two"""
    start = time.time()

    data = load_data("datasmall2")
    datastr = "".join([c for row in data for c in row])

    crops = {crop: datastr.count(crop) for crop in set(datastr)}
    crop_seen_plots = {crop:set() for crop in crops}
    crop_perimeters = {crop:{} for crop in crops}
    crop_region_sides = {crop:{} for crop in crops}
    crop_region_totals = {crop:{} for crop in crops}
    crop_region_plots = {crop:{} for crop in crops}
    
    directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]

    hits = [["." for _ in range(len(data[0])+2)] for _ in range(len(data)+2)]

    def check_dir(crop, point, crop_region):
        x, y = point
        if not 0 <= x < len(data[0]) or not 0 <= y < len(data):
            crop_seen_plots[crop].add(point)
            crop_perimeters[crop][crop_region] += 1
            return 0
        if data[y][x] != crop:
            crop_seen_plots[crop].add(point)
            crop_perimeters[crop][crop_region] += 1
            return 0
        if point in crop_seen_plots[crop]:
            crop_seen_plots[crop].add(point)
            return 0

        crop_region_plots[crop][crop_region].add(point)
        crop_seen_plots[crop].add(point)

        plot_hits = 0
        for direction in directions:
            plot_hits += check_dir(crop, (x + direction[0], y + direction[1]), crop_region)
        return plot_hits + 1

    for crop, crop_count in crops.items():
        crops_found = 0
        crop_region = 0
        while crops_found != crop_count:
            if crop_region not in crop_seen_plots[crop]:
                crop_perimeters[crop][crop_region] = 0
                crop_region_sides[crop][crop_region] = 0
                crop_region_totals[crop][crop_region] = 0
                crop_region_plots[crop][crop_region] = set()
            region_crops = 0
            crop_start_point = None
            for y in range(len(data)):
                for x in range(len(data[0])):
                    if (x, y) in crop_seen_plots[crop]: continue
                    if data[y][x] == crop:
                        crop_start_point = (x, y)
                        break
                else:
                    continue
                break
            region_crops = check_dir(crop, crop_start_point, crop_region)
            crops_found += region_crops
            crop_region_totals[crop][crop_region] = region_crops
            crop_region += 1
    
    total = 0

    for crop in crop_region_totals:
        region_totals = crop_region_totals[crop]
        region_perimeters = crop_perimeters[crop]
        for region in region_totals:
            total += region_totals[region] * region_perimeters[region]

    def is_surrounded(point, crop):
        for direction in directions:
            dx, dy = point[0] + direction[0], point[1] + direction[1]
            if not 0 <= dx < len(data[0]) or not 0 <= dy < len(data):
                return False
            if data[dy][dx] != crop:
                return False
        return True

    def find_open_plot_near_crop(points, crop):
        for point in points:
            for direction in directions:
                dx, dy = point[0] + direction[0], point[1] + direction[1]
                if 0 <= dx < len(data[0]) and 0 <= dy < len(data):
                    if data[dy][dx] != crop:
                        return (dx, dy)


    target = "C"
    sides = 0
    bot_moves = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0)
    }
    next_dir = {
        "^": (">", bot_moves[">"]),
        ">": ("v", bot_moves["v"]),
        "v": ("<", bot_moves["<"]),
        "<": ("^", bot_moves["^"]),
    }

    def rotate(dir):
        return next_dir[dir]

    for region in crop_region_plots[target]:
        plots = crop_region_plots[target][region]
        if len(plots) == 1:
            crop_region_sides[target][region] = 4
            break
        plots = [plot for plot in plots if not is_surrounded(plot, target)]
        for x, y in plots:
            hits[y+1][x+1] = "#"
        botx, boty = find_open_plot_near_crop(plots, target)
        botx += 1
        boty += 1
        bot_char = "^"
        bot_dir = bot_moves[bot_char]
        hits[boty][botx] = bot_char

        for row in hits:
            print(" ".join(row))
        time.sleep(2)
        # search clockwise
        while True:
            dx, dy = botx + bot_dir[0], boty + bot_dir[1]
            if 0 <= dx < len(hits[0]) and 0 <= dy < len(hits):
                if hits[dy][dx] == '.':
                    bots_right = next_dir[bot_char][1]
                    dxx, dyy = botx + bots_right[0], boty + bots_right[1]
                    if 0 <= dxx < len(hits[0]) and 0 <= dyy < len(hits):
                        if hits[dyy][dxx] == "#":
                            hits[dy][dx] = bot_char
                            hits[boty][botx] = "."
                            botx, boty = dx, dy
                        else:
                            bot_char, bot_dir = next_dir[bot_char]
                            hits[boty][botx] = bot_char
                            dxx, dyy = botx + bot_dir[0], boty + bot_dir[1]
                            print(hits[dyy][dxx])
                            if hits[dyy][dxx] == ".":
                                hits[dyy][dxx] = bot_char
                                hits[boty][botx] = "X"
                                botx, boty = dxx, dyy
                    else:
                        bot_char, bot_dir = next_dir[bot_char]
                        hits[boty][botx] = bot_char
                        dxx, dyy = botx + bot_dir[0], boty + bot_dir[1]
                        print(hits[dyy][dxx])
                        if hits[dyy][dxx] == ".":
                            hits[dyy][dxx] = bot_char
                            hits[boty][botx] = "X"
                            botx, boty = dxx, dyy
                else:
                    bot_char, bot_dir = next_dir[bot_char]
                    hits[boty][botx] = bot_char
                    dxx, dyy = botx + bot_dir[0], boty + bot_dir[1]
                    print(hits[dyy][dxx])
                    if hits[dyy][dxx] == ".":
                        hits[dyy][dxx] = bot_char
                        hits[boty][botx] = "X"
                        botx, boty = dxx, dyy
            else:
                bot_char, bot_dir = next_dir[bot_char]
                hits[boty][botx] = bot_char
                dxx, dyy = botx + bot_dir[0], boty + bot_dir[1]
                print(hits[dyy][dxx])
                if hits[dyy][dxx] == ".":
                    hits[dyy][dxx] = bot_char
                    hits[boty][botx] = "X"
                    botx, boty = dxx, dyy
            os.system("cls")
            print(bot_char, bot_dir, (botx, boty))
            for row in hits:
                print(" ".join(row))

            time.sleep(0.25)
            
            # next spot
            # can we go up?
            
            
        print()
        hits[pny][pnx] = "."

    print(crop_region_sides[target])

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
