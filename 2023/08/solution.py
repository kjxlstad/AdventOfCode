from functools import partial
from itertools import cycle
from math import lcm


def parse(data):
    def parse_elem(line):
        return line[:3], line[7:15].split(", ")

    instructions, network = data.split("\n\n")
    return instructions, dict(parse_elem(line) for line in network.split("\n"))


def find_path_length(elem, instructions, network, end_condition):
    for i, instruction in enumerate(cycle(instructions), start=1):
        next_index = 0 if instruction == "L" else 1
        elem = network[elem][next_index]
        if end_condition(elem):
            return i


if __name__ == "__main__":
    with open("data.in", "r") as f:
        instructions, network = parse(f.read())

    path_length = partial(find_path_length, instructions=instructions, network=network)

    # Part 1
    print(path_length("AAA", end_condition=lambda x: x == "ZZZ"))

    # Part 2
    path_lengths = [
        path_length(elem, end_condition=lambda x: x.endswith("Z"))
        for elem in network
        if elem.endswith("A")
    ]

    print(lcm(*path_lengths))
