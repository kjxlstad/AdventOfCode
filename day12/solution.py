from functools import reduce


def paths(current, visited=set(), twice=False, last=None):
    if current == "end":
        return 1

    if twice and current == "start" and visited:
        return 0

    if current.islower() and current in visited:
        if twice and last is None:
            last = current
        else:
            return 0

    return sum(
        paths(_next, visited | {current}, twice=twice, last=last)
        for _next in adjacency[current]
    )


def bi_adjacency(acc, new):
    return {
        **acc,
        new[0]: acc.get(new[0], []) + [new[1]],
        new[1]: acc.get(new[1], []) + [new[0]],
    }


if __name__ == "__main__":
    lines = [line.strip().split("-") for line in open("data.in", "r").readlines()]
    adjacency = reduce(bi_adjacency, lines, {})

    # Part 1
    print(paths("start"))

    # Part 2
    print(paths("start", twice=True))
