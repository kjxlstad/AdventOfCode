from collections import defaultdict, namedtuple
from heapq import heappush, heappop

Point = namedtuple("Point", ["x", "y"])


N, E, S, W = Point(0, -1), Point(+1, 0), Point(0, +1), Point(-1, 0)
TURNS = {N: [E, W], E: [N, S], S: [E, W], W: [N, S]}


def minimal_heat_loss(grid, start, end, min_straight, max_straight):
    w, h = len(grid[0]), len(grid)

    cost = defaultdict(lambda: float("inf"))
    queue = []

    for dir in TURNS:
        cost[(start, dir)] = 0
        heappush(queue, (0, start, dir))

    while queue:
        heat_loss, pos, vel = heappop(queue)

        if not (heat_loss <= cost[(pos, vel)]):
            continue

        for mag in range(1, max_straight + 1):
            new_pos = Point(pos.x + vel.x * mag, pos.y + vel.y * mag)

            if not (0 <= new_pos.x < w) or not (0 <= new_pos.y < h):
                break

            heat_loss += grid[new_pos.y][new_pos.x]

            for dir in TURNS[vel]:
                less_loss = heat_loss < cost[(new_pos, dir)]
                moved_enough = min_straight <= mag
                if less_loss and moved_enough:
                    cost[(new_pos, dir)] = heat_loss
                    heappush(queue, (heat_loss, new_pos, dir))

    return min(cost[(end, dir)] for dir in TURNS)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        grid = [[int(c) for c in line] for line in f.read().split("\n")]

    start = Point(0, 0)
    end = Point(len(grid[0]) - 1, len(grid) - 1)

    # Part 1
    print(minimal_heat_loss(grid, start, end, 1, 3))

    # Part 2
    print(minimal_heat_loss(grid, start, end, 4, 10))
