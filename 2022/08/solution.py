from functools import partial, reduce
from operator import mul


def scan(x, y, heightmap):
    # over, right, under, left
    return (
        [heightmap[i][x] for i in range(y - 1, -1, -1)],
        [heightmap[y][i] for i in range(x + 1, len(heightmap[0]))],
        [heightmap[i][x] for i in range(y + 1, len(heightmap))],
        [heightmap[y][i] for i in range(x - 1, -1, -1)],
    )


def is_visible(x, y, heightmap):
    # Any of the 4 directions has only trees lower than tree at x, y
    return any(
        all(heightmap[y][x] > h for h in direction)
        for direction in scan(x, y, heightmap)
    )


def view_distance(height, sightline):
    # Add 1 until tree in sightline is bigger than or equal to height
    if not sightline:
        return 0

    return 1 + (view_distance(height, sightline[1:]) if sightline[0] < height else 0)


def scenic_score(x, y, heightmap):
    # Product of the number of visible trees in each direction
    view = partial(view_distance, heightmap[y][x])
    return reduce(mul, map(view, scan(x, y, heightmap)))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        heightmap = [list(map(int, row)) for row in f.read().split("\n")]
        w, h = len(heightmap[0]), len(heightmap)

    # Part 1
    print(sum(is_visible(x, y, heightmap) for y in range(h) for x in range(w)))

    # Part 2
    print(max(scenic_score(x, y, heightmap) for y in range(h) for x in range(w)))
