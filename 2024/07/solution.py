from math import floor, log10
from operator import add, mul
from typing import Callable

BinOp = Callable[[int, int], int]


def parse_equation(line: str) -> tuple[int, list[int]]:
    a, *b = map(int, line.replace(":", "").split())
    return a, b


def concat(a: int, b: int) -> int:
    return a * 10 ** (floor(log10(b) + 1)) + b


def solvable(target: int, operands: list[int], ops: list[BinOp]) -> int:
    def solve(a: int, operands: list[int]) -> bool:
        if len(operands) == 0:
            return a == target

        b, *rest = operands

        for op in ops:
            if solve(op(a, b), rest):
                return True
        return False

    return solve(operands[0], operands[1:]) * target


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    equations = [parse_equation(line) for line in data]

    # Part 1
    print(sum(solvable(*eq, [add, mul]) for eq in equations))

    # Part 2
    print(sum(solvable(*eq, [add, mul, concat]) for eq in equations))
