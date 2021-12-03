from functools import reduce

data = [line.split(" ") for line in open("data/day02.in", "r").readlines()]
cmds = [(cmd, int(mag)) for cmd, mag in data]


# Part 1 & 2
actions = {
    "up":      lambda a, b: (a[0],     a[1],            a[2] - b),
    "down":    lambda a, b: (a[0],     a[1],            a[2] + b),
    "forward": lambda a, b: (a[0] + b, a[1] + a[2] * b, a[2]    ),
}


def move(state, cmd):
    cmd, mag = cmd
    return actions[cmd](state, mag)


pos, depth, aim = reduce(move, cmds, (0, 0, 0))
print(pos * aim)
print(pos * depth)
