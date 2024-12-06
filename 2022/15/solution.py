import re
from collections import defaultdict, namedtuple

Scanner = namedtuple("Scanner", ("x", "y", "r"))


def remaining(scanner, n, row, dist):
    min_y = min(scanner.y, scanner.y + dist)
    max_y = max(scanner.y, scanner.y + dist)
    if min_y <= row <= max_y:
        yield from range(scanner.x - n, scanner.x + n + 1)


def not_beacon(scanners, row):
    impossible = set()

    for scanner in scanners:
        impossible.update(
            val
            for y in (-scanner.r, scanner.r)
            for val in remaining(scanner, scanner.r - abs(row - scanner.y), row, y)
        )

    return len(impossible) - 1


def distress_beacon(scanners):
    rays = defaultdict(set)

    for scanner in scanners:
        rim = scanner.r + 1

        # find coeffs of rim rotated 45 degrees
        # perpendicular if coeffs are equal and with opposite rots
        # should be two of these, x marks the spot, their intersection is the beacon
        for dx, dy in (1, 1), (1, -1), (-1, 1), (-1, -1):
            coeff = scanner.x + dx * rim - dy * scanner.y
            rays[(dy, coeff)].add(dx)

    # fails for input cases where two scans share a rim on the very edge of the grid
    (m_0, a), (m_1, b) = (ray for ray, n in rays.items() if len(n) == 2)

    # Find gradient, intersection is then the only valid solution
    slope = (m_0 - m_1) // 2
    return slope * (a + b) // 2, slope * (b - a) // 2


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = f.read().split("\n")
    nums = [map(int, re.findall(r"-?\d+", line)) for line in lines]
    scanners = [
        (Scanner(s_x, s_y, abs(s_x - b_x) + abs(s_y - b_y)))
        for s_x, s_y, b_x, b_y in nums
    ]

    # Part 1
    print(not_beacon(scanners, 2_000_000))

    # Part 2
    x, y = distress_beacon(scanners)
    print(x * 4_000_000 + y)
