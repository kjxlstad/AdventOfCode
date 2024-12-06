from dataclasses import dataclass
from functools import partial
from multiprocessing import Pool
from typing import Iterator, Self


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Vec(self.x + other.x, self.y + other.y)


def patrol_protocol(pos: Vec, vel: Vec, obstructions: set[Vec]) -> tuple[Vec, Vec]:
    while (next_pos := pos + vel) in obstructions:
        vel = Vec(-vel.y, vel.x)

    return next_pos, vel


def patrol(
    pos: Vec, grid_size: Vec, obstructions: set[Vec]
) -> Iterator[tuple[Vec, Vec]]:
    vel = Vec(0, -1)

    while 0 <= pos.x < grid_size.x and 0 <= pos.y < grid_size.y:
        yield pos, vel
        pos, vel = patrol_protocol(pos, vel, obstructions)


def guard_visits(pos: Vec, grid_size: Vec, obstructions: set[Vec]) -> set[Vec]:
    return {pos for pos, _ in patrol(pos, grid_size, obstructions)}


def guard_loops(pos: Vec, grid_size: Vec, obstructions: set[Vec]) -> bool:
    visited = set()

    for pos, vel in patrol(pos, grid_size, obstructions):
        if (pos, vel) in visited:
            return True

        visited.add((pos, vel))

    return False


if __name__ == "__main__":
    lines = open("data.in").read().splitlines()
    grid = {Vec(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}

    grid_size = Vec(len(lines[0]), len(lines))
    obstructions = {pos for pos, char in grid.items() if char == "#"}
    start_pos = next(pos for pos, char in grid.items() if char == "^")

    # Part 1
    visited = guard_visits(start_pos, grid_size, obstructions)
    print(len(visited))

    # Part 2
    obstacles = (obstructions | {pos} for pos in visited if grid[pos] == ".")
    loops = Pool().map(partial(guard_loops, start_pos, grid_size), obstacles)
    print(sum(loops))
