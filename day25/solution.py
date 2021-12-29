from functools import reduce

PRECEDENCE = (">", "v")
BLANK = "."


def next_state(neighbors, herd):
    previous, current, next_ = neighbors

    if current == BLANK:
        return herd if previous == herd else current
    elif current == herd:
        return current if next_ != BLANK else BLANK

    return current


def step_herd(grid, herd):
    neighbors = lambda line, i: (line[(i + d) % len(line)] for d in (-1, 0, 1))

    return (
        tuple(next_state(neighbors(line, i), herd) for i, _ in enumerate(line))
        for line in grid
    )


def step(grid, n=1):
    next_grid = reduce(
        lambda grid, herd: tuple(zip(*step_herd(grid, herd))), PRECEDENCE, grid
    )

    return n if grid == next_grid else step(next_grid, n + 1)


if __name__ == "__main__":
    grid = (tuple(line.strip()) for line in open("data.in", "r").readlines())

    # Part 1
    print(step(grid))
