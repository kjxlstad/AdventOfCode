from functools import partial
from itertools import combinations


def find_empty_rows(image):
    return [i for i, row in enumerate(image) if row == "." * len(row)]


def transpose(image):
    return ["".join(row) for row in zip(*image)]


def manhattan_distance(p1, p2):
    return sum(abs(x - y) for x, y in zip(p1, p2))


def galaxy_distance(empty_rows, empty_cols, p1, p2, expansion):
    min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
    min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])

    empty_cols = [x for x in empty_cols if min_x <= x <= max_x]
    empty_rows = [y for y in empty_rows if min_y <= y <= max_y]

    return (
        manhattan_distance(p1, p2)
        + len(empty_cols) * (expansion - 1)
        + len(empty_rows) * (expansion - 1)
    )


if __name__ == "__main__":
    with open("data.in", "r") as image:
        image = image.read().split("\n")

    empty_rows = find_empty_rows(image)
    empty_cols = find_empty_rows(transpose(image))
    distance = partial(galaxy_distance, empty_rows, empty_cols)

    galaxies = [
        (x, y)
        for y, row in enumerate(image)
        for x, tile in enumerate(row)
        if tile == "#"
    ]
    pairs = list(combinations(galaxies, 2))

    # Part 1
    print(sum(distance(p1, p2, expansion=2) for p1, p2 in pairs))

    # Part 2
    print(sum(distance(p1, p2, expansion=1_000_000) for p1, p2 in pairs))
