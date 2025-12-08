from heapq import heapify, heappop, nlargest
from itertools import combinations, islice
from typing import Iterator, NamedTuple

from disjoint_set import DisjointSet

Box = NamedTuple("Box", [("x", int), ("y", int), ("z", int)])


def parse_box(line: str) -> Box:
    return Box(*map(int, line.split(",")))


def distance(a: Box, b: Box) -> int:
    return sum((u - v) ** 2 for u, v in zip(a, b))


def closest_pairs(nodes: list[Box]) -> Iterator[tuple[Box, Box]]:
    pairs = combinations(nodes, 2)
    pair_heap = [(distance(*p), p) for p in pairs]
    heapify(pair_heap)

    while pair_heap:
        _, (a, b) = heappop(pair_heap)
        yield a, b


if __name__ == "__main__":
    with open("data.in", "r") as f:
        boxes = list(map(parse_box, f.readlines()))

    circuit = DisjointSet[Box]({n: n for n in boxes})
    pairs = closest_pairs(boxes)

    # Part 1
    for a, b in islice(pairs, 1000):
        circuit.union(a, b)

    top_three = nlargest(3, map(len, circuit.itersets()))
    print(top_three[0] * top_three[1] * top_three[2])

    # Part 2
    while len(list(circuit.itersets())) > 1:
        a, b = next(pairs)
        circuit.union(a, b)

    print(a.x * b.x)
