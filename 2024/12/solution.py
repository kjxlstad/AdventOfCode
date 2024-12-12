from itertools import combinations
from typing import Iterator

DIRS = 1, -1, 1j, -1j
ORTHOGONAL_PAIRS = {pair for pair in combinations(DIRS, 2) if sum(pair)}


def neighbors(grid: dict[complex, str], pos: complex) -> set[complex]:
    return {next_pos for step in DIRS if grid.get(next_pos := pos + step) == grid[pos]}


def num_corners(grid: dict[complex, str], pos: complex) -> int:
    def is_corner(pair: tuple[complex, complex]) -> bool:
        adjecent = {grid.get(pos + step) for step in pair}
        diagonal = grid.get(pos + sum(pair))

        matches_current = {grid[pos] == adj for adj in adjecent}
        convex = not any(matches_current)
        concave = all(matches_current) and diagonal != grid[pos]

        return convex or concave

    return sum(is_corner(pair) for pair in ORTHOGONAL_PAIRS)


def explore_region(grid: dict[complex, str], start: complex) -> set[complex]:
    to_visit = {start}

    region = set()
    perimiter = 0
    sides = 0

    while to_visit:
        pos = to_visit.pop()
        adjecent = neighbors(grid, pos)

        region.add(pos)
        perimiter += 4 - len(adjecent)
        sides += num_corners(grid, pos)

        to_visit.update(adjecent - region)

    return region, perimiter, sides


def analyze_regions(grid: dict[complex, str]) -> Iterator[tuple[int, int, int]]:
    start_positions = set(grid)

    while start_positions:
        region, perimiter, sides = explore_region(grid, start_positions.pop())
        yield len(region), perimiter, sides
        start_positions -= region


if __name__ == "__main__":
    data = open("data.in").read().splitlines()

    grid = {x + y * 1j: c for y, row in enumerate(data) for x, c in enumerate(row)}
    stats = list(analyze_regions(grid))

    # Part 1
    print(sum(area * permiter for area, permiter, _ in stats))

    # Part 2
    print(sum(area * sides for area, _, sides in stats))
