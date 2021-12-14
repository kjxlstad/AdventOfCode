from functools import reduce


def parse(lines):
    points, folds = lines.split("\n\n")

    points = {tuple(int(ax) for ax in point.split(",")) for point in points.split("\n")}
    folds = [fold[11:].split("=") for fold in folds.split("\n")[:-1]]
    folds = [(fold[0], int(fold[1])) for fold in folds]

    return points, tuple(folds)


def fold(axis, crease, points):
    crease_range = lambda n: 2 * crease - n if n > crease else n

    if axis == "x":
        return {(crease_range(x), y) for x, y in points}

    return {(x, crease_range(y)) for x, y in points}


def fold_all(points, folds):
    points = reduce(lambda a, b: fold(*b, a), folds, points)

    x_max, y_max = max(x for x, _ in points), max(y for _, y in points)

    grid = [
        ["■" if (i, j) in points else " " for i in range(x_max + 1)]
        for j in range(y_max + 1)
    ]

    return grid


def pretty_print(grid):
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    lines = open("data.in", "r").read()

    points, folds = parse(lines)

    # Part 1
    print(len(fold(*folds[0], set(points))))

    # Part 2
    pretty_print(fold_all(points, folds))
