from functools import partial, reduce
from itertools import batched
from operator import mul
from re import findall
from typing import NamedTuple

Vec = NamedTuple("Vec", [("x", int), ("y", int)])
W, H = 101, 103


def parse_robot(robot: str) -> tuple[Vec, Vec]:
    nums = batched(map(int, findall(r"-?\d+", robot)), 2)
    return Vec(*next(nums)), Vec(*next(nums))


def elapse(pos: Vec, vel: Vec, seconds: int) -> Vec:
    new_x = (pos.x + vel.x * seconds) % W
    new_y = (pos.y + vel.y * seconds) % H
    return Vec(new_x, new_y)


def safety_factor(robots: list[tuple[Vec, Vec]], seconds: int) -> int:
    quadrants = [0] * 4

    for pos, vel in robots:
        x, y = elapse(pos, vel, seconds)

        quadrants[0] += x < W // 2 and y < H // 2
        quadrants[1] += x > W // 2 and y < H // 2
        quadrants[2] += x < W // 2 and y > H // 2
        quadrants[3] += x > W // 2 and y > H // 2

    return reduce(mul, quadrants)


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    robots = [parse_robot(robot) for robot in data]

    # Part 1
    print(safety_factor(robots, 100))

    # Part 2
    print(min(range(10_000), key=partial(safety_factor, robots)))
