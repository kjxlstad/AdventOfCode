from itertools import repeat
from operator import mul

import networkx


def parse_edges(line):
    src, *dsts = line.replace(":", "").split()
    return zip(repeat(src), dsts)


def partition_sizes(edges):
    graph = networkx.Graph(edges)
    _, partitions = networkx.stoer_wagner(graph)
    return mul(*map(len, partitions))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        edges = [edge for line in f.read().split("\n") for edge in parse_edges(line)]

    # Part 1
    print(partition_sizes(edges))
