from functools import reduce


def parse_stacks(stack_lines):
    # Split into lines, drop last
    lines = stack_lines.split("\n")[:-1]
    transposed = ["".join(s) for s in zip(*lines)]

    # Read each column except the last number row, strip empty spaces
    columns = [transposed[i].strip() for i in range(1, len(transposed), 4)]

    # Reverse, so top of stack is last element, enumerate columns starting at 1
    return {i: s[::-1] for i, s in enumerate(columns, start=1)}


def parse_move(move_line):
    # Split on space, ingore 'move', 'from', 'to'
    _, n, _, start, _, end = move_line.split(" ")
    return (*map(int, (n, start, end)),)


def move(stack, n, start, end):
    new_start = stack[start][:-n]
    new_end = stack[end] + stack[start][-n:]

    return {
        i: new_start if i == start else new_end if i == end else stack[i]
        for i in stack.keys()
    }


def move_single(stack, n, start, end):
    if n == 0:
        return stack

    return move_single(move(stack, 1, start, end), n - 1, start, end)


def apply(func, stacks, moves):
    return reduce(lambda r, m: func(r, *m), moves, stacks)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        stack_lines, move_lines = f.read().split("\n\n")

        stacks = parse_stacks(stack_lines)
        moves = [parse_move(move) for move in move_lines.split("\n")]

    # Part 1
    print("".join(s[-1] for s in apply(move_single, stacks, moves).values()))

    # Part 2
    print("".join(s[-1] for s in apply(move, stacks, moves).values()))
