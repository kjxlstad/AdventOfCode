from itertools import accumulate


def parse(txt: str) -> int:
    return int(txt.replace("L", "-").replace("R", "+"))


def turn_dial(pos: int, delta: int) -> int:
    return (pos + delta) % 100


def crosses(position: int, delta: int) -> int:
    if position == 0:
        return abs(delta) // 100

    if delta < 0:
        return (abs(delta) + 100 - position) // 100

    return (delta + position) // 100


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = f.read().splitlines()

    deltas = [parse(line) for line in lines]
    positions = list(accumulate(deltas, turn_dial, initial=50))

    # Part 1
    print(sum(1 for p in positions if p == 0))

    # Part 2
    print(sum(crosses(p, d) for p, d in zip(positions, deltas)))
