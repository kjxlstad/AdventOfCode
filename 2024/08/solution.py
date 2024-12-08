from itertools import combinations
from typing import Iterator


def parse_map(data: list[str]) -> dict[str, set[complex]]:
    grid = {x + y * 1j: c for y, line in enumerate(data) for x, c in enumerate(line)}
    freqs = set(grid.values()) - {"."}

    return {freq: {n for n in grid if grid[n] == freq} for freq in freqs}


def antenna_pairs(antennas: dict[str, set[complex]]) -> Iterator[complex]:
    for _, positions in antennas.items():
        yield from combinations(positions, 2)


def on_grid(n: complex, w: int, h: int) -> bool:
    return 0 <= n.real < w and 0 <= n.imag < h


def antinodes(antennas: dict[str, set[complex]], w: int, h: int) -> set[complex]:
    nodes = set()

    for a, b in antenna_pairs(antennas):
        nodes.add(2 * a - b)
        nodes.add(2 * b - a)

    return {n for n in nodes if on_grid(n, w, h)}


def harmonics(a: complex, b: complex, w: int, h: int) -> Iterator[complex]:
    current, diff = a, b - a

    while on_grid(current, w, h):
        yield current
        current += diff


def harmonic_antinodes(
    antennas: dict[str, set[complex]], w: int, h: int
) -> set[complex]:
    nodes = set()

    for a, b in antenna_pairs(antennas):
        nodes.update(harmonics(a, b, w, h))
        nodes.update(harmonics(b, a, w, h))

    return nodes


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    w, h = len(data[0]), len(data)
    antennas = parse_map(data)

    # Part 1
    print(len(antinodes(antennas, w, h)))

    # Part 2
    print(len(harmonic_antinodes(antennas, w, h)))
