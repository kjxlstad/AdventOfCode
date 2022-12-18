from functools import cache
from itertools import product, tee
from collections import defaultdict


def floyd_warshall_fill(valves, distances):
    for k, i, j in product(*tee(valves, 3)):
        distances[i, j] = min(
            distances[i, j], distances[i, k] + distances[k, j]
        )


def parse_valves(lines):
    valves, flow_rates = set(), {}
    edges = defaultdict(lambda: float("inf"))

    for node, flow_rate, edges_ in lines:
        valves.add(node)
        if flow_rate:
            flow_rates[node] = flow_rate
        for edge in edges_:
            edges[node, edge] = 1

    floyd_warshall_fill(valves, edges)
    return flow_rates, edges


def max_flow(time, flow_rates, edges, elephant=False):
    @cache
    def search(t, v="AA", us=frozenset(flow_rates), e=False):
        flow = [
            search(t - 1 - edges[v, u], u, us - {u}, e)
            + flow_rates[u] * (t - 1 - edges[v, u])
            for u in us
            if edges[v, u] < t
        ]

        return max(flow + [search(26, us=us) if e else 0])

    return search(time, e=elephant)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        data = [
            (w[1], int(w[4].strip("rate=;")), [s.strip(",") for s in w[9:]])
            for w in map(str.split, f.read().split("\n"))
        ]

    flow_rates, edges = parse_valves(data)

    # Part 1
    print(max_flow(30, flow_rates, edges))

    # Part 2
    print(max_flow(26, flow_rates, edges, elephant=True))
