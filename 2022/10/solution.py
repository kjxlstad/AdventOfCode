def execute(instruction, register):
    match instruction.split(" "):
        case ["addx", x]:
            return [register[-1], register[-1] + int(x)]
        case _:
            return [register[-1]]


def cycle(instructions):
    register = [1]

    for instruction in instructions:
        register += execute(instruction, register)

    return register


def signal_strengths(register_values):
    return [register_values[i] * (i + 1) for i in range(19, 220, 40)]


def pixel(register, x):
    lit = x in [register - 1, register, register + 1]
    return "⬜" if lit else "⬛"


def render(register_values):
    pixels = [
        [pixel(register_values[y * 40 + x], x) for x in range(40)]
        for y in range(6)
    ]
    return "\n".join("".join(row) for row in pixels)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = f.read().split("\n")

    register = cycle(lines)

    # Part 1
    print(sum(signal_strengths(register)))

    # Part 2
    print(render(register))
