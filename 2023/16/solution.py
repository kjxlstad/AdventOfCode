from collections import deque, namedtuple
from itertools import chain

Point = namedtuple("Point", ["x", "y"])


N, E, S, W = Point(0, -1), Point(+1, 0), Point(0, +1), Point(-1, 0)

REFLECTIONS = {
    ".": {N: [N], E: [E], S: [S], W: [W]},
    "/": {N: [E], E: [N], S: [W], W: [S]},
    "\\": {N: [W], E: [S], S: [E], W: [N]},
    "|": {N: [N], E: [N, S], S: [S], W: [N, S]},
    "-": {N: [E, W], E: [E], S: [E, W], W: [W]},
}


def fire_laser(grid, pos, vel):
    w, h = len(grid[0]), len(grid)

    (queue := deque()).append((pos, vel))
    energized = {(pos, vel)}

    while queue:
        pos, vel = queue.pop()
        tile = grid[pos.y][pos.x]

        for vel in REFLECTIONS[tile][vel]:
            pos = Point(pos.x + vel.x, pos.y + vel.y)
            in_grid = (0 <= pos.x < w) and (0 <= pos.y < h)
            visited = (pos, vel) in energized
            if in_grid and not visited:
                energized.add((pos, vel))
                queue.append((pos, vel))

    return {pos for pos, _ in energized}


def starting_configurations(grid):
    w, h = len(grid[0]), len(grid)

    west = ((Point(0 + 0, y), E) for y in range(h))
    east = ((Point(w - 1, y), W) for y in range(h))
    north = ((Point(x, 0 + 0), S) for x in range(w))
    south = ((Point(x, h - 1), N) for x in range(w))

    yield from chain(west, east, north, south)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        grid = [list(line) for line in f.read().split("\n")]

    # Part 1
    print(len(fire_laser(grid, Point(0, 0), E)))

    # Part 2
    energy_levels = (
        len(fire_laser(grid, pos, vel)) for pos, vel in starting_configurations(grid)
    )
    print(max(energy_levels))
