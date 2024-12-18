from bisect import bisect_left
from collections import defaultdict
from functools import partial
from math import inf


def exit_steps(memory: list[complex], fallen_bytes: int) -> int:
    corrupted = set(memory[:fallen_bytes])
    entry, exit = 0, 70 + 70j

    queue = [(0, entry)]
    dists = defaultdict(lambda: inf) | {entry: 0}

    def within_bounds(pos: complex) -> bool:
        return 0 <= pos.real <= 70 and 0 <= pos.imag <= 70

    while queue:
        dist, pos = queue.pop(0)

        neighbors = (pos + step for step in {1, -1, 1j, -1j})
        neighbors = set(filter(within_bounds, neighbors))

        for pos in neighbors - corrupted:
            if (new_dist := dist + 1) < dists[pos]:
                dists[pos] = new_dist
                queue.append((new_dist, pos))

    return dists[exit]


def first_blocking_byte(memory: list[complex]) -> complex:
    search_space = range(1024, len(memory))
    first_blocking = bisect_left(search_space, inf, key=partial(exit_steps, memory))
    return memory[first_blocking + search_space.start - 1]


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    memory = [complex(*map(int, line.split(","))) for line in data]

    # Part 1
    print(exit_steps(memory, 1024))

    # Part 2
    blocker = first_blocking_byte(memory)
    print(f"{int(blocker.real)},{int(blocker.imag)}")
