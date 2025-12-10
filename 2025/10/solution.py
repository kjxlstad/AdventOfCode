from typing import Any, Callable

import z3


def parse_machine(line: str) -> tuple[list[bool], list[set[int]], list[int]]:
    first, *mid, last = line.split()

    indicators = [int(c == "#") for c in first[1:-1]]
    wiring = [{int(n) for n in part[1:-1].split(",")} for part in mid]
    joltage = [int(n) for n in last[1:-1].split(",")]

    return indicators, wiring, joltage


def minimum_button_presses(
    targets: list[int],
    wiring: list[set[int]],
    constraint: Callable[[Any, int], Any],
) -> list[int]:
    solver = z3.Optimize()
    presses = z3.IntVector("presses", len(wiring))

    solver.add([press >= 0 for press in presses])

    for i, target in enumerate(targets):
        total = sum(press for press, wire in zip(presses, wiring) if i in wire)
        solver.add(constraint(total, target))

    solver.minimize(sum(presses))

    if solver.check() != z3.sat:
        raise ValueError("No solution found")

    model = solver.model()
    return [model.evaluate(press).as_long() for press in presses]


if __name__ == "__main__":
    with open("data.in", "r") as f:
        machines = [parse_machine(line) for line in f]

    # Part 1
    toggle_presses = (
        minimum_button_presses(lights, wiring, lambda p, t: p % 2 == t)
        for lights, wiring, _ in machines
    )
    print(sum(map(sum, toggle_presses)))

    # Part 2
    level_presses = (
        minimum_button_presses(joltage, wiring, lambda p, t: p == t)
        for _, wiring, joltage in machines
    )
    print(sum(map(sum, level_presses)))
