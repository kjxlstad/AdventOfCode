from collections import namedtuple
from itertools import pairwise, accumulate, starmap

Vec = namedtuple("Point", ["x", "y"])

def add(vec0, vec1):  return Vec(vec0.x + vec1.x, vec0.y + vec1.y)
def mul(vec, scalar): return Vec(vec.x * scalar, vec.y * scalar)
def det(vec0, vec1):  return vec0.x * vec1.y - vec1.x * vec0.y

DIRECTION_NAMES = {"U": Vec(0, -1), "R": Vec(+1, 0), "D": Vec(0, +1), "L": Vec(-1, 0)}
DIRECTION_NUMS = {i: vec for i, vec in enumerate(DIRECTION_NAMES.values())}


def parse_line(line):
    direction, magnitude, color = line.split(" ")
    direction = DIRECTION_NAMES[direction]
    return direction, int(magnitude), color[2:-1]


def swap_instructions(color):
    *magnitude, direction = [c for c in color]
    direction = DIRECTION_NUMS[int(direction)]
    return direction, int("".join(str(d) for d in magnitude), 16)


def total_area(vertices, boundary_length):
    polygon_area = sum(starmap(det, pairwise(vertices))) // 2
    return polygon_area + boundary_length // 2 + 1


def lagoon_volume(dirs, mags):
    moves = (mul(dir, mag) for dir, mag in zip(dirs, mags))
    vertices = accumulate(moves, add)
    return total_area(vertices, sum(mags) + 1)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        lines = [parse_line(line) for line in f.read().split("\n")]

    # Part 1
    dirs, mags, _ = zip(*lines)
    print(lagoon_volume(dirs, mags))

    # Part 2
    dirs, mags = zip(*[swap_instructions(color) for *_, color in lines])
    print(lagoon_volume(dirs, mags))
