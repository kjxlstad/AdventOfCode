from networkx import Graph, enumerate_all_cliques


def construct_network(data: str) -> Graph:
    network = Graph()
    network.add_edges_from(line.split("-") for line in data)
    return network


def inter_connected_computers(subnets: list[list[str]], size: int, prefix: str) -> int:
    return len(
        [c for c in subnets if len(c) == size and any(n.startswith(prefix) for n in c)]
    )


def lan_password(subnets: list[list[str]]) -> str:
    largest_subnet = max(subnets, key=len)
    return ",".join(sorted(largest_subnet))


if __name__ == "__main__":
    network = construct_network(open("data.in").read().splitlines())

    subnets = list(enumerate_all_cliques(network))

    # Part 1
    print(inter_connected_computers(subnets, size=3, prefix="t"))

    # Part 2
    print(lan_password(subnets))
