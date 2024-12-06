from collections import namedtuple
from functools import reduce
from re import findall

span = namedtuple("span", ["min", "max"])
cube = namedtuple("cube", ["x", "y", "z"])
step = namedtuple("step", ["state", "cube"])


def count(steps, volume):
    if not steps:
        return 0

    step, *rest = steps

    if step.state == "off":
        return count(rest, volume)

    return (
        volume(step.cube)
        + count(rest, volume)
        - count(
            {intersection(step.cube, other.cube) for other in rest} - {None}, volume
        )
    )


def intersection(a, b):
    x = span(max(a.x.min, b.x.min), min(a.x.max, b.x.max))
    y = span(max(a.y.min, b.y.min), min(a.y.max, b.y.max))
    z = span(max(a.z.min, b.z.min), min(a.z.max, b.z.max))

    if x.min <= x.max and y.min <= y.max and z.min <= z.max:
        return step(..., cube(x, y, z))


def volume(cube):
    return reduce(lambda a, b: a * (b.max - b.min + 1), cube, 1)


def bound_volume(cube, bounding_cube=cube(*((span(-50, 50),) * 3))):
    bounded_cube = intersection(cube, bounding_cube)
    return volume(bounded_cube.cube) if bounded_cube is not None else 0


def parse(line):
    state, new = line.split()
    points = list(map(int, findall(r"-?\d+", new)))
    return step(state, cube(*[span(*points[i : i + 2]) for i in range(0, 6, 2)]))


if __name__ == "__main__":
    instructions = tuple(map(parse, open("data.in", "r")))

    # Part 1
    print(count(instructions, bound_volume))

    # Part 2
    print(count(instructions, volume))
