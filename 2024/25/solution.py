from itertools import product


def parse_schematic(schematic: str) -> tuple[bool, list[int]]:
    grid = [list(row) for row in schematic.splitlines()]
    return grid[0] == list("#####"), [col.count("#") - 1 for col in zip(*grid)]


def fits(key: list[int], lock: list[int]) -> bool:
    return all(k + l <= 5 for k, l in zip(key, lock))


if __name__ == "__main__":
    schematics = open("data.in").read().split("\n\n")
    parsed = list(map(parse_schematic, schematics))

    keys = [pins for is_key, pins in parsed if is_key]
    locks = [pins for is_key, pins in parsed if not is_key]

    # Part 1
    print(sum(fits(key, lock) for key, lock in product(keys, locks)))
