from itertools import count


def transpose(platform):
    return [list(col) for col in zip(*platform)]


def rotate(platform):
    return transpose(platform)[::-1]


def as_transposed(func, matrix, *args):
    # Transpose before and after to use roll_west as roll_south
    return transpose(func(transpose(matrix), *args))


def window(row):
    padded = (None, *row, None)
    return zip(padded, padded[1:], padded[2:])


def next_state(prev, curr, next):
    match curr:
        case "O": return "." if prev == "." else "O"
        case ".": return "O" if next == "O" else "."
        case "#": return "#"


def roll_row(row):
    new = [next_state(*state) for state in window(row)]
    return row if row == new else roll_row(new)


def roll_west(platform):
    return [roll_row(row) for row in platform]


def load(platform):
    return sum(
        row.count("O") * (len(row) - i)
        for i, row in enumerate(platform)
    )


def cycle_once(platform):
    for _ in "NWSE":
        platform = rotate(roll_west(platform))
    return platform


def cycle(platform, n):
    seen = [platform]

    for c in count(start=1):
        if (platform := cycle_once(platform)) in seen:
            # exploit repeating pattern if seen before
            i = seen.index(platform)
            return seen[i + (n - i) % (c - i)]

        seen.append(platform)

    return platform


if __name__ == "__main__":
    with open("data.in", "r") as platform:
        platform = [list(row) for row in platform.read().split("\n")]

    # Part 1
    print(load(as_transposed(roll_west, platform)))

    # Part 2
    print(load(as_transposed(cycle, platform, 1_000_000_000)))
