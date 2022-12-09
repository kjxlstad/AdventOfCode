def step(direction):
    return {"R": 1, "L": -1, "U": 1j, "D": -1j}[direction]


def chebychev_distance(head, tail):
    return max(abs(head.real - tail.real), abs(head.imag - tail.imag))


def sign(n):
    return (n > 0) - (n < 0)


def sign_c(c):
    return sign(c.real) + sign(c.imag) * 1j


def follow(head, tail):
    if chebychev_distance(head, tail) <= 1:
        return tail

    return tail + sign_c(head - tail)


def visits(moves, length):
    rope = [0 for _ in range(length)]
    visited = {0}

    for direction, steps in moves:
        for _ in range(steps):
            rope[0] += step(direction)
            for i in range(1, len(rope)):
                rope[i] = follow(rope[i - 1], rope[i])

            visited.add(rope[-1])

    return len(visited)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = f.read().split("\n")
        moves = [(a, int(b)) for a, b in map(str.split, lines)]

    # Part 1
    print(visits(moves, 2))

    # Part 2
    print(visits(moves, 10))
