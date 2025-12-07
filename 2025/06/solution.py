from functools import partial, reduce
from itertools import pairwise, starmap
from operator import mul

product = partial(reduce, mul)


def parse_operator(operator_row: str) -> list[tuple[str, int, int]]:
    operator_row += " !"

    operator_positions = [
        (operator, idx) for idx, operator in enumerate(operator_row) if operator != " "
    ]

    return [
        (operator, start, next_start - 2)
        for (operator, start), (_, next_start) in pairwise(operator_positions)
    ]


def parse_chunks(rows: list[str]):
    *number_rows, operator_row = rows

    chunks = parse_operator(operator_row)

    operators, problem_grids = zip(
        *[
            (operator, [list(line[start : end + 1]) for line in number_rows])
            for operator, start, end in chunks
        ]
    )

    return operators, problem_grids


def solve_problem(numbers: list[list[str]], operator: str) -> int:
    operation = sum if operator == "+" else product
    parsed_numbers = [int("".join(row)) for row in numbers]
    return operation(parsed_numbers)


def transpose(grid: list[list[str]]) -> list[list[str]]:
    return [list(col) for col in zip(*grid)]


if __name__ == "__main__":
    with open("data.in", "r") as f:
        operators, chunks = parse_chunks(f.read().splitlines())

    # Part 1
    total = sum(starmap(solve_problem, zip(chunks, operators)))
    print(total)

    # Part 2
    transposed_chunks = map(transpose, chunks)
    print(sum(starmap(solve_problem, zip(transposed_chunks, operators))))
