from functools import lru_cache
from itertools import starmap


def parse_line(line):
    springs, hints = line.split(" ")
    return springs, tuple(int(c) for c in hints.split(","))


def unfold(springs, hints):
    return "?".join([springs] * 5), hints * 5


@lru_cache(maxsize=None)
def arrangements(springs, hints):
    # If the hints are emtpy then we have two cases
    if not len(hints):
        # 1. Springs not covered by hints, impossible, nullify this branch
        # 2. All springs covered by hints, we are done
        return int("#" not in springs)

    # If the leftover hints cover more than the remaining springs
    # then it is impossible to satisfy the hints, nullify this branch
    if sum(hints) > len(springs):
        return 0

    # Doesnt chagne the result
    if springs[0] == ".":
        return arrangements(springs[1:], hints)

    num = 0
    # Here we have some freedom, either we start the block of springs here,
    # or we start it later.
    # 1. Add the number of arrangements if we start later
    if springs[0] == "?":
        num += arrangements(springs[1:], hints)

    # 2. Add the number of arrangements if we start here
    # If we start here, then we consume the springs covered by this hint
    consumed, rest = springs[: hints[0]], springs[hints[0] :]
    sep, non_consumed = rest[:1], rest[1:]

    # We can only consume if it contains no empty .
    if all(c != "." for c in consumed):
        # Can only consume if the spring after the hint is empty . or wildcard ?
        if not len(sep) or sep[0] in ".?":
            num += arrangements(non_consumed, hints[1:])

    return num


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = [parse_line(line) for line in f.read().split("\n")]

    # Part 1
    print(sum(starmap(arrangements, lines)))

    # Part 2
    print(sum(starmap(arrangements, starmap(unfold, lines))))
