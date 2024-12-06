from functools import reduce
from itertools import count


def transpose(platform):
    return [list(col) for col in zip(*platform)]


def rotate(platform):
    return transpose(platform)[::-1]


def as_transposed(func):
    # Transpose before and after to use roll_west as roll_south
    def wrapper(matrix, *args):
        return transpose(func(transpose(matrix), *args))

    return wrapper


def tilt_west(platform):
    def roll(part):
        return "O" * part.count("O") + "." * part.count(".")

    return [
        "#".join(roll(part) for part in "".join(row).split("#")) for row in platform
    ]


def load(platform):
    return sum(row.count("O") * (len(row) - i) for i, row in enumerate(platform))


def cycle_once(platform):
    return reduce(lambda p, _: rotate(tilt_west(p)), "NWSE", platform)


@as_transposed
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
    tilt_north = as_transposed(tilt_west)
    print(load(tilt_north(platform)))

    # Part 2
    print(load(cycle(platform, 1_000_000_000)))
