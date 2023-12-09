from itertools import pairwise
from operator import add, sub


def extrapolate(sequence, accum):
    if all(s == 0 for s in sequence):
        return 0

    diff = [b - a for a, b in pairwise(sequence)]
    return accum(extrapolate(diff, accum), sequence[-1])


if __name__ == "__main__":
    with open("data.in") as oasis_report:
        sequences = [
            [int(n) for n in line.split()]
            for line in oasis_report.read().split("\n")
        ]

    # Part 1
    print(sum(extrapolate(sequence, add) for sequence in sequences))

    # Part 2
    print(sum(-extrapolate(sequence[::-1], sub) for sequence in sequences))
