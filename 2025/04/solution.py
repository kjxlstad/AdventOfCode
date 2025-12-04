from itertools import product


def neighbors(pos: complex, rolls: set[complex]) -> set[complex]:
    offsets = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}
    return {pos + complex(dx, dy) for dx, dy in offsets} & rolls


def accessible(rolls: set[complex]) -> set[complex]:
    return {pos for pos in rolls if len(neighbors(pos, rolls)) < 4}


def num_removable(rolls: set[complex]) -> int:
    removable = accessible(rolls)

    if not removable:
        return 0

    return len(removable) + num_removable(rolls - removable)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = f.read().splitlines()

    rolls = {
        complex(x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == "@"
    }

    # Part 1
    print(len(accessible(rolls)))

    # Part 2
    print(num_removable(rolls))
