from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
Target = namedtuple("Target", ["min", "max"])


def in_target(target, pos):
    return target.min.x <= pos.x <= target.max.x and target.min.y <= pos.y <= target.max.y


def step(pos, vel):
    return Point(pos.x + vel.x, pos.y + vel.y), Point(
        vel.x + [-1, 0, 1][(vel.x < 0) + (vel.x <= 0)], vel.y - 1
    )


def trajectory(pos, vel, target):
    if abs(pos.x) <= max(abs(target.min.x), abs(target.max.x)) and target.min.y <= pos.y:
        return in_target(target, pos) or trajectory(*step(pos, vel), target)

    return False


def trick_shots(target):
    return sum(
        trajectory(Point(0, 0), Point(x_vel, y_vel), target)
        for x_vel in range(0, max(target.max.x, 0) + 1)
        for y_vel in range(target.min.y, abs(target.max.y) * 2 + 1)
    )


if __name__ == "__main__":
    data = open("data.in", "r").read().strip()[13:].split(", ")

    target = Target(
        Point(*(int(c.split("..")[0][2:]) for c in data)),
        Point(*(int(c.split("..")[1]) for c in data)),
    )

    # Part 1
    print(min(target.max.y, target.min.y) * -~min(target.max.y, target.min.y) // 2)

    # Part 2
    print(trick_shots(target))
