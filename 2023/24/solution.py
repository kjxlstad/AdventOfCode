from collections import namedtuple
from itertools import combinations

from z3 import And, IntVector, Solver

Vec = namedtuple("Vec", "x y z")
Ray = namedtuple("Ray", "pos vel")

MIN, MAX = 2e14, 4e14


def parse_hailstone(line):
    pos, vel = line.replace(" ", "").split("@")
    pos = Vec(*map(int, pos.split(",")))
    vel = Vec(*map(int, vel.split(",")))
    return Ray(pos, vel)


def intersects(ray0, ray1):
    p1, p2 = ray0.pos, ray1.pos
    v1, v2 = ray0.vel, ray1.vel

    if v1.y * v2.x == v2.y * v1.x:
        return False

    dx, dy = p1.x - p2.x, p1.y - p2.y
    t1 = (v2.y * dx - v2.x * dy) / (v1.y * v2.x - v1.x * v2.y)
    t2 = (v1.x * dy - v1.y * dx) / (v2.y * v1.x - v2.x * v1.y)

    x, y = p1.x + v1.x * t1, p1.y + v1.y * t1

    in_test_area = MIN <= x <= MAX and MIN <= y <= MAX
    in_future = t1 > 0 and t2 > 0

    return in_test_area and in_future


def determine_rock_throw(hailstones):
    rock_pos = IntVector("rock_pos", 3)
    rock_vel = IntVector("rock_vel", 3)
    collision_times = IntVector("t", 3)

    constraints = [
        rock_pos[d] + rock_vel[d] * t == hail_pos[d] + hail_vel[d] * t
        for t, (hail_pos, hail_vel) in zip(collision_times, hailstones)
        for d in range(3)
    ]

    solver = Solver()
    solver.add(And(constraints))
    solver.check()
    model = solver.model()

    return (model[p].as_long() for p in rock_pos)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        hailstones = [parse_hailstone(line) for line in f.read().split("\n")]

    # Part 1
    print(sum(intersects(a, b) for a, b in combinations(hailstones, 2)))

    # Part 2
    print(sum(determine_rock_throw(hailstones)))
