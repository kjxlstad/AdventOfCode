from bisect import bisect_left
from collections import defaultdict
from functools import partial
from math import inf
from typing import NamedTuple


class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)

    def __str__(self) -> str:
        return f"{self.x},{self.y}"


DIRECTIONS = {Vec(1, 0), Vec(-1, 0), Vec(0, 1), Vec(0, -1)}


def exit_steps(memory: list[Vec], fallen_bytes: int) -> int:
    corrupted = set(memory[:fallen_bytes])
    entry, exit = Vec(0, 0), Vec(70, 70)

    queue = [(0, entry)]
    dists = defaultdict(lambda: inf) | {entry: 0}

    def within_bounds(pos: Vec) -> bool:
        return 0 <= pos.x <= 70 and 0 <= pos.y <= 70

    while queue:
        dist, pos = queue.pop(0)

        neighbors = (pos + step for step in DIRECTIONS)
        neighbors = set(filter(within_bounds, neighbors))

        for pos in neighbors - corrupted:
            if (new_dist := dist + 1) < dists[pos]:
                dists[pos] = new_dist
                queue.append((new_dist, pos))

    return dists[exit]


def first_blocking_byte(memory: list[Vec]) -> Vec:
    search_space = range(1024, len(memory))
    first_blocking = bisect_left(search_space, inf, key=partial(exit_steps, memory))
    return memory[first_blocking + search_space.start - 1]


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    memory = [Vec(*map(int, line.split(","))) for line in data]

    # Part 1
    print(exit_steps(memory, 1024))

    # Part 2
    print(first_blocking_byte(memory))
