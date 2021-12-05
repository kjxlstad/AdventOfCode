from functools import reduce


def vertical_cover(line):
    x = line[0][0]
    ys = list(zip(*line))[1]

    return ((x, y) for y in range(min(ys), max(ys) + 1))


def horizontal_cover(line):
    def flip(line):
        return [p[::-1] for p in line]

    return flip(vertical_cover(flip(line)))


def diagonal_cover(line):
    dirs = [1 if line[0][ax] < line[1][ax] else -1 for ax in {0, 1}]

    x_range, y_range = [
        range(ax[0], ax[1] + dirs[i], dirs[i]) for i, ax in enumerate(zip(*line))
    ]

    return (p for p in zip(x_range, y_range))


def cover(line, include_diag=False):
    # Vertical
    if line[0][0] == line[1][0]:
        return vertical_cover(line)

    # Horizontal
    elif line[0][1] == line[1][1]:
        return horizontal_cover(line)

    # Diagonal
    elif include_diag:
        return diagonal_cover(line)

    # Bin diagonals
    else:
        return ()


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
