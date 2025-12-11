from functools import cache, reduce
from itertools import pairwise
from operator import mul

type Node = str


def parse_node(line: str) -> tuple[str, list[str]]:
    device, outputs = line.split(": ")
    return device, outputs.split()


def num_paths(graph: dict[str, list[str]], start: Node, end: Node) -> int:
    @cache
    def paths_from(current: Node) -> int:
        if current == end:
            return 1
        return sum(paths_from(output) for output in graph.get(current, []))

    return paths_from(start)


def num_paths_through(graph: dict[str, list[str]], nodes: list[Node]) -> int:
    return reduce(mul, (num_paths(graph, src, dst) for src, dst in pairwise(nodes)))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        graph = {device: outputs for device, outputs in map(parse_node, f.readlines())}

    # Part 1
    print(num_paths(graph, "you", "out"))

    # Part 2
    sequences = (["svr", "dac", "fft", "out"], ["svr", "fft", "dac", "out"])
    print(sum(num_paths_through(graph, seq) for seq in sequences))
