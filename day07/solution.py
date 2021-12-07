def constant_cost(a, b):
    return abs(a - b)


def incremental_cost(a, b):
    return sum(range(1, constant_cost(a, b) + 1))


def fuel_costs(crabs, target, cost_func):
    return sum([count * cost_func(pos, target) for pos, count in crabs.items()])


def minimum_cost(crabs, cost_func):
    targets = range(min(crabs), max(crabs) + 1)
    total_costs = [fuel_costs(crabs, target, cost_func) for target in targets]

    return min(total_costs)


if __name__ == "__main__":
    crabs = [int(pos) for pos in open("data.in", "r").read().split(",")]

    # Collect crabs with common position, reduces overhead with ~40%
    crab_positions = {pos: crabs.count(pos) for pos in crabs}

    # Very inefficient as of now, part 2 takes a few seconds to run
    print(minimum_cost(crab_positions, constant_cost))
    print(minimum_cost(crab_positions, incremental_cost))
