from itertools import chain, pairwise


def below(x, y):
    yield from ((x + dx, y + 1) for dx in (0, -1, 1))


def air(pos, floor, rocks, sand):
    return pos[1] != floor and pos not in rocks and pos not in sand


def poured_until_abyss(rocks, limit):
    sand = set()

    def trickle(x, y):
        for pos in below(x, y):
            if air(pos, limit + 1, rocks, sand):
                return trickle(*pos)

        return x, y

    while all(s[1] < limit for s in sand):
        sand |= {trickle(500, 0)}

    return len(sand) - 1


def poured_until_full(rocks, limit):
    def fill(x, y, sand=set()):
        if air((x, y), limit + 2, rocks, sand):
            sand |= {(x, y)}
            return 1 + sum(fill(*pos, sand) for pos in below(x, y))

        return 0

    return fill(500, 0)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        points = [
            [tuple(map(int, point.split(","))) for point in line.split("->")]
            for line in f.read().split("\n")
        ]

    segments = chain.from_iterable(pairwise(line) for line in points)
    rocks = {
        (x, y)
        for (x_0, y_0), (x_1, y_1) in segments
        for x in range(min(x_0, x_1), max(x_0, x_1) + 1)
        for y in range(min(y_0, y_1), max(y_0, y_1) + 1)
    }
    limit = max(y for _, y in rocks)

    # Part 1
    print(poured_until_abyss(rocks, limit))

    # Part 2
    print(poured_until_full(rocks, limit))
