from z3 import Solver, Int, Not, Or, And, sat
from rich.progress import track


def parse_line(line):
    springs, groups = line.split(" ")
    return springs, [int(c) for c in groups.split(",")]


def add_constraints(solver, springs, groups):
    N = len(springs)
    num_groups = len(groups)

    group_starts = [Int(f"start_{i}") for i in range(num_groups)]
    group_ends = [Int(f"end_{i}") for i in range(num_groups)]

    # Encode facts
    for k in range(N):
        if springs[k] == ".":
            # An empty cell can't be part of any group
            empty_constraints = [
                And(start <= k, k <= end)
                for start, end in zip(group_starts, group_ends)
            ]
            solver.add(Not(Or(empty_constraints)))

        elif springs[k] == "#":
            # A filled cell must be within a group
            filled_constraints = [
                And(start <= k, k <= end)
                for start, end in zip(group_starts, group_ends)
            ]
            solver.add(Or(filled_constraints))

    # Encode constraints
    for i in range(num_groups):
        # All starts must be on [0, N)
        solver.add(0 <= group_starts[i], group_starts[i] < N)
        # All ends must be on [0, N)
        solver.add(0 <= group_ends[i], group_ends[i] < N)
        # Difference between start and end is group size minus one
        solver.add(group_ends[i] - group_starts[i] == groups[i] - 1)

    # The gap between the end of one group and the start of the next >= 2
    for i in range(num_groups - 1):
        solver.add(group_starts[i + 1] >= group_ends[i] + 2)

    return group_starts, group_ends


def format_model(model, group_start, group_end, N):
    solution = ["."] * N
    for start, end in zip(group_start, group_end):
        start = model[start].as_long()
        end = model[end].as_long()
        for j in range(start, end + 1):
            solution[j] = "#"

    return "".join(solution)


def find_all_models(springs, groups):
    solver = Solver()
    group_starts, group_ends = add_constraints(solver, springs, groups)
    N = len(springs)

    while solver.check() == sat:
        model = solver.model()
        yield format_model(model, group_starts, group_ends, N)

        # Add a constraint to block the current solution
        block_constraint = [
            Or(start != model[start], end != model[end])
            for start, end in zip(group_starts, group_ends)
        ]
        solver.add(Or(block_constraint))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = [parse_line(line) for line in f.read().split("\n")]

    springs = "?###????????"
    groups = [3, 2, 1]

    for model in find_all_models(springs, groups):
        print(model)

    num_models = sum(
        len(list(find_all_models(springs, blocks)))
        for springs, blocks in track(lines)
    )

    print(num_models)
