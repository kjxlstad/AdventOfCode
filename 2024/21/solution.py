from functools import cache, partial, reduce
from itertools import pairwise, starmap
from operator import add
from typing import NamedTuple

Pos = NamedTuple("Position", [("x", int), ("y", int)])

DPAD_BUTTONS = " ^A", "<v>"
DPAD = {c: Pos(x, y) for y, row in enumerate(DPAD_BUTTONS) for x, c in enumerate(row)}

NUMPAD_BUTTONS = "789", "456", "123", " 0A"
NUMPAD = {
    c: Pos(x, y) for y, row in enumerate(NUMPAD_BUTTONS) for x, c in enumerate(row)
}


def fewest_presses(code: str, depth: int, layer: int = 0) -> int:
    comp = partial(sequence_length, depth=depth, layer=layer)
    return reduce(add, starmap(comp, pairwise("A" + code)))


def move_sequence(start: Pos, end: Pos) -> tuple[str, str]:
    x_dir, y_dir = "<>"[end.x > start.x], "^v"[end.y > start.y]
    x_diff, y_diff = abs(start.x - end.x), abs(start.y - end.y)
    horizontal_moves = x_dir * x_diff
    vertical_moves = y_dir * y_diff
    return (
        horizontal_moves + vertical_moves + "A",
        vertical_moves + horizontal_moves + "A",
    )


@cache
def sequence_length(start_char: str, end_char: str, depth: int, layer: int) -> int:
    if layer == depth:
        return 1

    coords = NUMPAD if layer == 0 else DPAD
    start_pos, end_pos, gap_pos = map(coords.get, (start_char, end_char, " "))

    horizontal_first, vertical_first = move_sequence(start_pos, end_pos)
    candidates = []

    if (end_pos.x, start_pos.y) != gap_pos:
        candidates.append(fewest_presses(horizontal_first, depth, layer + 1))

    if (start_pos.x, end_pos.y) != gap_pos:
        candidates.append(fewest_presses(vertical_first, depth, layer + 1))

    return min(candidates)


if __name__ == "__main__":
    codes = open("data.in").read().splitlines()

    # Part 1
    print(sum(fewest_presses(code, 3) * int(code[:-1]) for code in codes))

    # Part 2
    print(sum(fewest_presses(code, 26) * int(code[:-1]) for code in codes))
