from re import finditer

DIGITS = (*map(str, range(0, 10)),)
NON_SYMBOLS = ".", *DIGITS
GEAR = "*"


def find_parts(schematic):
    return [
        (row, match)
        for row, line in enumerate(schematic)
        for match in finditer(r"\d+", line)
    ]


def find_neighbours(row, part):
    x_range = range(part.start(0) - 1, part.end(0) + 1)
    y_range = range(row - 1, row + 2)

    symbol = int(part.group(0))
    return (symbol, [(x, y) for x in x_range for y in y_range])


def find_gears(neighbours):
    return [
        [part for (part, neighbours) in neighbours if pos in neighbours]
        for pos, symbol in map_.items()
        if symbol == GEAR
    ]


if __name__ == "__main__":
    with open("data.in", "r") as f:
        schematic = f.read().split("\n")

    map_ = {
        (x, y): char for y, line in enumerate(schematic) for x, char in enumerate(line)
    }

    parts = find_parts(schematic)
    part_neighbours = [find_neighbours(*part) for part in parts]

    # Part 1
    print(
        sum(
            part
            for (part, neighbours) in part_neighbours
            if any(map_.get(c, ".") not in NON_SYMBOLS for c in neighbours)
        )
    )

    # Part 2
    gears = find_gears(part_neighbours)
    print(sum(ratios[0] * ratios[1] for ratios in gears if len(ratios) == 2))
