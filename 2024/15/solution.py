from functools import reduce

DIRS = {">": 1, "<": -1, "^": -1j, "v": 1j}


def parse_grid(grid_data: str, resize: bool = False) -> dict[complex, str]:
    if resize:
        swaps = str.maketrans({"#": "##", ".": "..", "O": "[]", "@": "@."})
        grid_data = grid_data.translate(swaps)

    return {
        x + y * 1j: c
        for y, row in enumerate(grid_data.split())
        for x, c in enumerate(row)
    }


def move(grid: dict[complex, str], pos: complex, step: complex) -> bool:
    copy = grid.copy()

    def swap(a: complex, b: complex) -> bool:
        grid[a], grid[b] = grid[b], grid[a]
        return True

    def _move(pos, step):
        next_pos = pos + step
        cell = grid[next_pos]

        conds = (
            cell == ".",
            cell == "O" and _move(next_pos, step),
            cell == "[" and _move(next_pos + 1, step) and _move(next_pos, step),
            cell == "]" and _move(next_pos - 1, step) and _move(next_pos, step),
        )

        return swap(pos, next_pos) if any(conds) else False

    return (grid, pos + step) if _move(pos, step) else (copy, pos)


def navigate(grid_data: str, moves: list[complex], resize: bool = False) -> int:
    grid = parse_grid(grid_data, resize)
    pos = next(p for p in grid if grid[p] == "@")
    return reduce(lambda state, step: move(*state, step), moves, (grid, pos))[0]


def gps_coordinates_sum(grid: dict[complex, str]) -> int:
    return int(sum(pos.real + pos.imag * 100 for pos in grid if grid[pos] in "O["))


if __name__ == "__main__":
    grid_data, moves = open("data.in").read().split("\n\n")
    moves = [DIRS[m] for m in moves.replace("\n", "")]

    # Part 1
    print(gps_coordinates_sum(navigate(grid_data, moves)))

    # Part 2
    print(gps_coordinates_sum(navigate(grid_data, moves, resize=True)))
