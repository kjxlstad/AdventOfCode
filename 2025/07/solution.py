from functools import reduce


def step_particle(timelines: list[int], manifold_slice: str) -> list[int]:
    new_timelines = [0] * len(manifold_slice)
    for idx, cell in enumerate(manifold_slice):
        if cell == ".":
            new_timelines[idx] += timelines[idx]
        elif cell == "^":
            new_timelines[idx - 1] += timelines[idx]
            new_timelines[idx + 1] += timelines[idx]
    return new_timelines


def count_splits(timelines: list[int], manifold: list[str]) -> int:
    if not manifold:
        return 0

    row, *rest = manifold

    new_timelines = step_particle(timelines, row)
    splits = sum(new < old for new, old in zip(new_timelines, timelines))
    return splits + count_splits(new_timelines, rest)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        start, *manifold = f.read().splitlines()[::2]

    initial_timelines = [int(sym == "S") for sym in start]

    # Part 1
    print(count_splits(initial_timelines, manifold))

    # Part 2
    print(sum(reduce(step_particle, manifold, initial_timelines)))
