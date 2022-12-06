def constant_cost(a, b):
    return abs(a - b)


def incremental_cost(a, b):
    diff = constant_cost(a, b)
    return diff * (diff + 1) // 2


def fuel_costs(crabs, target, cost_func):
    return sum(count * cost_func(pos, target) for pos, count in crabs.items())


def minimum_cost(crabs, cost_func):
    targets = range(min(crabs), max(crabs) + 1)
    return min(fuel_costs(crabs, target, cost_func) for target in targets)


if __name__ == "__main__":
    crabs = tuple(map(int, open("data.in", "r").read().split(",")))

    # Collect crabs with common position, reduces overhead with ~40%
    crab_positions = {pos: crabs.count(pos) for pos in set(crabs)}

    print(minimum_cost(crab_positions, constant_cost))
    print(minimum_cost(crab_positions, incremental_cost))
