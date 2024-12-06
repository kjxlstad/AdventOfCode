from functools import reduce
from itertools import zip_longest


def cover(line, include_diag=False):
    dirs = [1 if line[0][ax] <= line[1][ax] else -1 for ax in {0, 1}]

    x_range, y_range = [
        range(ax[0], ax[1] + dirs[i], dirs[i]) for i, ax in enumerate(zip(*line))
    ]

    # In case of horizontal or vertical pad zip with the stationary value
    fill = list(x_range)[0] if len(x_range) == 1 else list(y_range)[0]
    diagonal = len(x_range) != 1 and len(y_range) != 1

    if diagonal and not include_diag:
        return ()

    return (p for p in zip_longest(x_range, y_range, fillvalue=fill))


def count_unique(acc, new):
    acc[new] = acc.get(new, 0) + 1
    return acc


def count_dangerous(lines, include_diag):
    # Accumulate the covered tiles for each line
    line_coverage = (tuple(cover(line, include_diag)) for line in lines)

    # Flatten and count occurrences of each position
    coverage = reduce(count_unique, reduce(lambda a, b: a + b, line_coverage), {})

    # Filter out dangerous positions
    dangerous = [pos for pos in coverage if coverage[pos] >= 2]

    return len(dangerous)


if __name__ == "__main__":
    data = [line.strip() for line in open("data.in", "r").readlines()]

    # Transform each line to [[x, y], [x, y]]
    lines = [
        [[int(ax) for ax in point.split(",")] for point in line.split(" -> ")]
        for line in data
    ]

    print(count_dangerous(lines, False))
    print(count_dangerous(lines, True))
