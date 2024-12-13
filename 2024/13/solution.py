from itertools import batched, starmap
from re import findall
from typing import Iterator, NamedTuple

Vector = NamedTuple("Vector", [("x", int), ("y", int)])


def parse_game(game: str) -> Iterator[Vector]:
    xy_pairs = batched(findall(r"\d+", game), 2)
    return [Vector(int(x), int(y)) for x, y in xy_pairs]


def cost_to_win(a: Vector, b: Vector, p: Vector) -> int:
    determinant = a.x * b.y - b.x * a.y
    a_presses, a_remainder = divmod(p.x * b.y - b.x * p.y, determinant)
    b_presses, b_remainder = divmod(a.x * p.y - p.x * a.y, determinant)

    if a_remainder or b_remainder:
        return 0

    return 3 * a_presses + b_presses


if __name__ == "__main__":
    data = open("data.in").read().split("\n\n")
    games = [parse_game(game) for game in data]

    # Part 1
    print(sum(starmap(cost_to_win, games)))

    # Part 2
    ERROR = 10**13
    games = ((*btns, Vector(p.x + ERROR, p.y + ERROR)) for *btns, p in games)
    print(sum(starmap(cost_to_win, games)))
