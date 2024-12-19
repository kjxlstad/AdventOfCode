from functools import lru_cache
from typing import Callable, Iterable


def arrangements(
    towels: list[str],
    patterns: list[str],
    reduction: Callable[[Iterable[int]], int] = any,
) -> int:
    @lru_cache
    def designs(towel: str) -> int:
        if not towel:
            return 1

        matches = (towel.removeprefix(p) for p in patterns if towel.startswith(p))
        return reduction(map(designs, matches))

    return sum(map(designs, towels))


if __name__ == "__main__":
    patterns, towels = open("data.in").read().split("\n\n")
    patterns = patterns.split(", ")
    towels = towels.splitlines()

    # Part 1
    print(arrangements(towels, patterns))

    # Part 2
    print(arrangements(towels, patterns, sum))
