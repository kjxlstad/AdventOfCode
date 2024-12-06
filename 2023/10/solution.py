from itertools import pairwise

N, E, S, W = (0, -1), (+1, 0), (0, +1), (-1, 0)

# (pipe, prev_move): next_move
MOVES = {
    ("|", S): S,
    ("|", N): N,
    ("-", E): E,
    ("-", W): W,
    ("L", W): N,
    ("L", S): E,
    ("J", E): N,
    ("J", S): W,
    ("7", E): S,
    ("7", N): W,
    ("F", W): S,
    ("F", N): E,
}

CONNECTIONS = {
    N: "|7F",
    S: "|LJ",
    W: "-FL",
    E: "-J7",
}


def determine_start_pipe(tiles, x, y):
    for (dx, dy), pipes in CONNECTIONS.items():
        nx, ny = x + dx, y + dy
        if tiles[ny][nx] in pipes:
            return "-" if dx else "|", (dx, dy)


def find_path(tiles, x, y):
    pipe, (dx, dy) = determine_start_pipe(tiles, x, y)
    start_x, start_y = x, y
    path = [(x, y)]

    while True:
        dx, dy = MOVES[pipe, (dx, dy)]
        x, y = x + dx, y + dy
        if (x, y) == (start_x, start_y):
            break
        pipe = tiles[y][x]
        path.append((x, y))

    return path


def find_area(path):
    # Needs to wrap around back to the start
    path_around = path + [path[0]]
    return (
        sum(x_0 * y_1 - x_1 * y_0 for ((x_0, y_0), (x_1, y_1)) in pairwise(path_around))
        // 2
    )


def enclosed_area(area, boundary_length):
    return area - boundary_length // 2 + 1


if __name__ == "__main__":
    with open("data.in", "r") as f:
        tiles = f.read().split("\n")

    start_tile = next(
        (x, y)
        for y, row in enumerate(tiles)
        for x, tile in enumerate(row)
        if tile == "S"
    )

    path = find_path(tiles, *start_tile)
    path_length = len(path)

    # Part 1
    print(path_length // 2)

    # Part 2
    print(enclosed_area(find_area(path), path_length))
