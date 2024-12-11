from functools import cache
from math import ceil, log10


def magnitude(n: int) -> int:
    return ceil(log10(n + 1))


@cache
def blink(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return blink(1, blinks - 1)

    if (num_digits := magnitude(stone)) % 2 == 0:
        left, right = divmod(stone, 10 ** (num_digits // 2))
        return blink(left, blinks - 1) + blink(right, blinks - 1)

    return blink(stone * 2024, blinks - 1)


if __name__ == "__main__":
    stones = [int(rock) for rock in open("data.in").read().split()]

    # Part 1
    print(sum(blink(stone, 25) for stone in stones))

    # Part 2
    print(sum(blink(stone, 75) for stone in stones))
