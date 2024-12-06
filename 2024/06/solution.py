from functools import partial
from multiprocessing import Pool
from typing import Iterator

Path = Iterator[tuple[complex, complex]]


def patrol(start: complex, w: int, h: int, obstructions: set[complex]) -> Path:
    pos, vel = start, -1j

    while 0 <= pos.real < w and 0 <= pos.imag < h:
        yield pos, vel

        while (next_pos := pos + vel) in obstructions:
            vel *= 1j

        pos = next_pos


def guard_loops(guard_path: Path, obstructions: set[complex]) -> bool:
    visited = set()

    for pos, vel in guard_path(obstructions):
        if (pos, vel) in visited:
            return True

        visited.add((pos, vel))

    return False


if __name__ == "__main__":
    lines = open("data.in").read().splitlines()
    grid = {x + y * 1j: c for y, line in enumerate(lines) for x, c in enumerate(line)}

    w, h = len(lines[0]), len(lines)
    obstructions = {pos for pos, char in grid.items() if char == "#"}
    start_pos = next(pos for pos, char in grid.items() if char == "^")

    # Part 1
    guard_path = partial(patrol, start_pos, w, h)
    visited = {pos for pos, _ in guard_path(obstructions)}
    print(len(visited))

    # Part 2
    obstacles = (obstructions | {pos} for pos in visited - {start_pos})
    loops = Pool().map(partial(guard_loops, guard_path), obstacles)
    print(sum(loops))
