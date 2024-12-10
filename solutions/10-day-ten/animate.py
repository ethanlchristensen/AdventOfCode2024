from bruhanimate import Screen, Buffer
from bruhcolor import bruhcolored as bc
import time
import uuid
import random

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


def run(screen: Screen):
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    color_mapping = {
        "0": 232,
        "1": 234,
        "2": 236,
        "3": 238,
        "4": 240,
        "5": 242,
        "6": 244,
        "7": 246,
        "8": 248,
        "9": 250,
    }

    data = load_data()

    tiles_traversed = {}

    erm = [[" " for _ in range(len(data[0]))] for _ in range(len(data))]

    def get_total_found_paths():
        output = 0
        for k, v in tiles_traversed.items():
            output += v["times_hit_9"]
        return output

    def get_padding_x_y():
        return((screen.width - (len(data[0]))) // 2, (screen.height - len(data)) // 2)
    
    padding_x, padding_y = get_padding_x_y()

    for y in range(len(data)):
        # offset_x = 0
        for x in range(len(data[0])):
            screen.print_at(
                text=bc(text=" ", on_color=color_mapping[data[y][x]]).colored,
                x=x + padding_x,
                y=y + padding_y,
                width=1
            )
            # offset_x += 1

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
                        new_value = data[dy][dx]
                        padding_x, padding_y = get_padding_x_y()
                        text = f"Total Valid Paths: {get_total_found_paths()}"
                        text_2 = f"Checking trailhead: {trail_head_id}"
                        screen.print_at(text=text, x=0, y=0, width=len(text))
                        screen.print_at(text=text_2, x=0, y=1, width=len(text_2))
                        screen.print_at(text="Trail Head Stats:", x=0, y=2, width=len("Trail Head Stats:"))
                        offset_y = 0
                        offset_x = 0
                        for idx, k in enumerate(tiles_traversed):
                            if idx % (screen.height - 3) == 0 and idx != 0:
                                offset_x += 1
                                offset_y = 0
                            text_3 = f"{k[:4]}: {tiles_traversed[k]['times_hit_9']}"
                            screen.print_at(text=text_3, x=offset_x * 9, y=3+offset_y, width=len(text_3))
                            offset_y += 1
                        screen.print_at(text=bc(text="*", color=tiles_traversed[trail_head_id]["color"], on_color=color_mapping[new_value]).colored, x=dx + padding_x, y=dy+ padding_y, width=1)
                        time.sleep(0.01)
                        check_dir(new_value, dx, dy, directions[0], trail_head_id)
                        check_dir(new_value, dx, dy, directions[1], trail_head_id)
                        check_dir(new_value, dx, dy, directions[2], trail_head_id)
                        check_dir(new_value, dx, dy, directions[3], trail_head_id)
    trail_heads = find_all_trail_heads(data=data)

    for trail_head in trail_heads:
        trail_head_id = str(uuid.uuid4())
        erm[trail_head[1]][trail_head[0]] = "0"
        tiles_traversed[trail_head_id] = {"times_hit_9": 0, "seen_xy": [], "color": random.randint(0, 255)}
        padding_x, padding_y = get_padding_x_y()
        screen.print_at(text=bc(text=" ", color=tiles_traversed[trail_head_id]["color"], on_color=color_mapping["0"]).colored, x=trail_head[0] + padding_x, y=trail_head[1] + padding_y, width=1)
        check_dir("0", trail_head[0], trail_head[1], directions[0], trail_head_id)
        check_dir("0", trail_head[0], trail_head[1], directions[1], trail_head_id)
        check_dir("0", trail_head[0], trail_head[1], directions[2], trail_head_id)
        check_dir("0", trail_head[0], trail_head[1], directions[3], trail_head_id)

    input()


if __name__ == "__main__":
    Screen.show(run)