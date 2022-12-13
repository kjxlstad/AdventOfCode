from functools import cmp_to_key
from ast import literal_eval


def compare(left, right):
    match left, right:
        case  int(),  int(): return left - right
        case  int(), list(): return compare([left], right)
        case list(),  int(): return compare(left, [right])
    return next(filter(bool, map(compare, left, right)), len(left) - len(right))


def divide(pairs, *dividers):
    packets = [p for pair in pairs for p in pair] + list(dividers)
    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    return [sorted_packets.index(d) + 1 for d in dividers]


if __name__ == "__main__":
    with open("data.in", "r") as f:
        pairs = [
            [literal_eval(x) for x in pair.split("\n")]
            for pair in f.read().split("\n\n")
        ]

    # Part 1
    print(sum(i + 1 for i, p in enumerate(pairs) if compare(*p) < 0))

    # Part 2
    idx_1, idx_2 = divide(pairs, [[2]], [[6]])
    print(idx_1 * idx_2)
