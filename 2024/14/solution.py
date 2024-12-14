from functools import partial, reduce
from itertools import batched
from operator import itemgetter, mul
from re import findall
from typing import NamedTuple

Vec = NamedTuple("Vec", [("x", int), ("y", int)])
Robot = NamedTuple("Robot", [("pos", Vec), ("vel", Vec)])
W, H = 101, 103


def parse_robot(robot: str) -> Robot:
    nums = batched(map(int, findall(r"-?\d+", robot)), 2)
    return Robot(Vec(*next(nums)), Vec(*next(nums)))


def elapse(robots: list[Robot], seconds: int = 1) -> list[Robot]:
    def step(robot: Robot) -> Robot:
        new_x = (robot.pos.x + robot.vel.x * seconds) % W
        new_y = (robot.pos.y + robot.vel.y * seconds) % H
        return Robot(Vec(new_x, new_y), robot.vel)

    return [step(robot) for robot in robots]


def safety_factor(robots: list[Robot]) -> int:
    def between(p, lower, upper):
        return lower.x <= p.x < upper.x and lower.y <= p.y < upper.y

    quadrant_checks = [
        partial(between, lower=Vec(0, 0), upper=Vec(W // 2, H // 2)),
        partial(between, lower=Vec(W // 2 + 1, 0), upper=Vec(W, H // 2)),
        partial(between, lower=Vec(0, H // 2 + 1), upper=Vec(W // 2, H)),
        partial(between, lower=Vec(W // 2 + 1, H // 2 + 1), upper=Vec(W, H)),
    ]

    quadrant_counts = (
        sum(quadrant(robot.pos) for robot in robots) for quadrant in quadrant_checks
    )

    return reduce(mul, quadrant_counts)


def deviation(robots: list[Robot], seconds: int) -> int:
    return sum(
        abs(robot.pos.x - W // 2) + abs(robot.pos.y - H // 2)
        for robot in elapse(robots, seconds)
    )


def min_deviation_time(robots: list[Robot], max_seconds: int = 10_000) -> int:
    deviations = ((s, deviation(robots, s)) for s in range(1, max_seconds))
    return min(deviations, key=itemgetter(1))[0]


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    robots = [parse_robot(robot) for robot in data]

    # Part 1
    print(safety_factor(elapse(robots, 100)))

    # Part 2
    print(min_deviation_time(robots))
