from functools import reduce
from itertools import permutations
from math import ceil
from collections import namedtuple

# Instead of dealing with trees, parse input into value and depth
number = namedtuple("number", ("value", "depth"))


def parse_depths(num, depth=0):
    if not len(num):
        return []

    literal, *rest = num

    DEPTH_CHANGE = {"[": 1, " ": 0, ",": 0, "]": -1}

    if literal in DEPTH_CHANGE:
        return parse_depths(rest, depth + DEPTH_CHANGE[literal])

    return [number(int(literal), depth)] + parse_depths(rest, depth)


def explode(num):
    pairs = [
        (i, left, right)
        for i, (left, right) in enumerate(zip(num, num[1:]))
        if left.depth == right.depth > 4
    ]

    if not len(pairs):
        return False, num

    i, left, right = pairs[0]

    start, end = num[:i], num[i + 2 :]

    if i > 0:
        start[-1] = number(start[-1].value + left.value, start[-1].depth)
    if i < len(num) - 2:
        end[0] = number(end[0].value + right.value, end[0].depth)

    return True, start + [number(0, left.depth - 1)] + end


def split(num):
    to_split = [(i, num) for i, num in enumerate(num) if num.value >= 10]

    if not len(to_split):
        return False, num

    i, num = to_split[0]

    insert = [
        number(num.value // 2, num.depth + 1),
        number(ceil(num.value / 2), num.depth + 1),
    ]

    return True, num[:i] + insert + num[i + 1 :]


def add(a, b):
    def reduce(num):
        for action in (explode, split):
            changed, num = action(num)
            if changed:
                return reduce(num)

        return num

    return reduce([number(num.value, num.depth + 1) for num in a + b])


def magnitude(num):
    if not len(num):
        return num[0][0]

    pairs = [
        (i, left, right)
        for i, (left, right) in enumerate(zip(num, num[1:]))
        if left.depth == right.depth
    ]

    if not len(pairs):
        return num[0][0]

    i, left, right = pairs[0]
    insert = [number(left.value * 3 + right.value * 2, left.depth - 1)]

    return magnitude(num[:i] + insert + num[i + 2 :])


if __name__ == "__main__":
    numbers = [line.strip() for line in open("data.in", "r").readlines()]
    depth_pairs = [parse_depths(number) for number in numbers]

    # Part 1
    print(magnitude(reduce(add, depth_pairs)))

    # Part 2
    print(max(magnitude(add(a, b)) for a, b in permutations(depth_pairs, 2)))
