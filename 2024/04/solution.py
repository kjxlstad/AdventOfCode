from itertools import product, batched
from typing import Iterator

DIAGS = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
CARDINALS = {(1, 0), (0, 1), (-1, 0), (0, -1)}
DIRECTIONS = DIAGS | CARDINALS


def substrings(grid: dict[tuple[int, int], str]) -> Iterator[list[str]]:
    for (x, y), (dx, dy) in product(grid, DIRECTIONS):
        yield [grid.get((x + dx * i, y + dy * i), "") for i in range(4)]


def blocks(grid: dict[tuple[int, int], str]) -> Iterator[list[str]]:
    for (x, y), (dx, dy) in product(grid, DIAGS):
        yield [grid.get((x + dx * i, y + dy * i), "") for i in (-1, 0, 1)]


def is_x_mas_block(diags: Iterator[list[str]]) -> bool:
    return sum(diag == list("MAS") for diag in diags) == 2


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    grid = {(i, j): s for i, row in enumerate(data) for j, s in enumerate(row)}

    # Part 1
    print(sum(s == list("XMAS") for s in substrings(grid)))

    # Part 2
    print(sum(map(is_x_mas_block, batched(blocks(grid), 4))))
