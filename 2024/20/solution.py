from itertools import product
from typing import Iterator


def advance(track: set[complex], pos: complex, vel: complex) -> tuple[complex, complex]:
    turns = vel * 1j, vel * -1j
    new_vel = next((vel for vel in turns if pos + vel in track), vel)
    return pos + new_vel, new_vel


def race(track: set[complex], start: complex, end: complex) -> Iterator[complex]:
    pos, vel = start, next(turn for turn in {1, -1, 1j, -1j} if start + turn in track)

    while pos != end:
        yield pos
        pos, vel = advance(track, pos, vel)

    yield pos


def offsets(max_dist: int) -> Iterator[complex]:
    def bounded_range(center: int, diameter: int) -> range:
        return range(center - diameter, center + diameter + 1)

    return (
        complex(x, y)
        for x in bounded_range(0, max_dist)
        for y in bounded_range(0, max_dist - abs(x))
    )


def shortcuts(dists: dict[complex, int], max_cut: int) -> Iterator[int]:
    for start, offset in product(dists, offsets(max_cut)):
        if (end := start + offset) in dists:
            dist = abs(start.real - end.real) + abs(start.imag - end.imag)
            yield dists[end] - dists[start] - dist


if __name__ == "__main__":
    data = open("data.in").read().splitlines()

    grid = {x + y * 1j: s for y, row in enumerate(data) for x, s in enumerate(row)}

    def find_char(char: str) -> Iterator[complex]:
        return (pos for pos, s in grid.items() if s == char)

    start, end = map(next, map(find_char, "SE"))
    track = set(find_char(".")) | {start, end}

    dists = {pos: i for i, pos in enumerate(race(track, start, end), 1)}

    # Part 1
    print(sum(dist_saved >= 100 for dist_saved in shortcuts(dists, 2)))

    # Part 2
    print(sum(dist_saved >= 100 for dist_saved in shortcuts(dists, 20)))
