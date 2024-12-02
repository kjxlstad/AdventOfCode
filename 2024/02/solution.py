from itertools import pairwise


def safe(levels: list[int]) -> bool:
    diffs = {a - b for a, b in pairwise(levels)}
    return diffs <= {1, 2, 3} or diffs <= {-1, -2, -3}


def almost_safe(levels: list[int]) -> bool:
    return any(safe(levels[:i] + levels[i + 1 :]) for i, _ in enumerate(levels))


if __name__ == "__main__":
    lines = open("data.in").read().splitlines()
    reports = [[int(x) for x in line.split()] for line in lines]

    # Part 1
    print(sum(map(safe, reports)))

    # Part 2
    print(sum(map(almost_safe, reports)))
