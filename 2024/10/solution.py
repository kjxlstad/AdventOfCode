from typing import Iterator


def neighbors(topo: dict[complex, int], pos: complex) -> Iterator[complex]:
    for step in 1, -1, 1j, -1j:
        if topo.get(next_pos := pos + step, 0) == topo[pos] + 1:
            yield next_pos


def trail_peaks(topo: dict[complex, int], trailhead: complex) -> Iterator[complex]:
    stack = [trailhead]

    while stack:
        pos = stack.pop()

        if topo[pos] == 9:
            yield pos

        stack.extend(neighbors(topo, pos))


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    topo = {x + y * 1j: int(h) for y, row in enumerate(data) for x, h in enumerate(row)}

    trailheads = (pos for pos, c in topo.items() if c == 0)
    trailhead_peaks = [list(trail_peaks(topo, start)) for start in trailheads]

    # Part 1
    print(sum(len(set(tp)) for tp in trailhead_peaks))

    # Part 2
    print(sum(len(tp) for tp in trailhead_peaks))
