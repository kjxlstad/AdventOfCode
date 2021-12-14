from functools import reduce


def neighbors(x, y):
    x_range = range(max(x - 1, 0), min(x + 2, 10))
    y_range = range(max(y - 1, 0), min(y + 2, 10))
    return {(x, y) for x in x_range for y in y_range} - {(x, y)}


def flashed_neighbors(grid, x, y):
    n = neighbors(x, y)

    return [
        [v + 1 if (i, j) in n else v for i, v in enumerate(row)]
        for j, row in enumerate(grid)
    ]


def flash(grid, flashed=set()):
    flashes = {
        (i, j)
        for j, row in enumerate(grid)
        for i, v in enumerate(row)
        if v > 9 and (i, j) not in flashed
    }

    grid = reduce(
        lambda acc, coords: flashed_neighbors(acc, coords[0], coords[1]), flashes, grid,
    )

    if flashes:
        return flash(grid, flashed | flashes)

    return grid, len(flashed)


def propagate(grid):
    grid = [[v + 1 for v in row] for row in grid]

    grid, flashes = flash(grid)

    grid = [[0 if v > 9 else v for v in row] for row in grid]

    return grid, flashes


if __name__ == "__main__":
    grid = [[int(n) for n in line.strip()] for line in open("data.in", "r").readlines()]

    # Part 1
    def chain(acc, _):
        a, b = propagate(acc[0])
        return a, acc[1] + b

    print(reduce(chain, range(100), (grid, 0))[1])

    # Part 2
    def resonant_iteration(grid, steps=1):
        grid, flashes = propagate(grid)

        if flashes != 100:
            return resonant_iteration(grid, steps + 1)

        return steps

    print(resonant_iteration(grid))
