from collections import defaultdict
from heapq import heappop, heappush
from typing import Iterator, Mapping, NamedTuple


class Vec(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Vec":
        return Vec(self.x * other, self.y * other)


EAST = Vec(1, 0)
DIRS = [EAST, Vec(0, 1), Vec(-1, 0), Vec(0, -1)]

type State = tuple[Vec, Vec]


def parse_grid(lines: list[str]) -> tuple[set[Vec], Vec, Vec]:
    grid = {Vec(x, y): c for y, row in enumerate(lines) for x, c in enumerate(row)}
    walls = {pos for pos, c in grid.items() if c == "#"}
    start = next(pos for pos, c in grid.items() if c == "S")
    end = next(pos for pos, c in grid.items() if c == "E")

    return walls, start, end


def moves(pos: Vec, vel: Vec, direction: int = 1):
    yield pos + vel * direction, vel, 1
    yield pos, Vec(vel.y, -vel.x), 1000
    yield pos, Vec(-vel.y, vel.x), 1000


def explore_maze(walls: set[Vec], start: Vec) -> int:
    queue, costs = [], defaultdict(lambda: float("inf"))

    # Yields new positions and velocities with associated total cost
    # if the move is valid and cheaper than the current best cost
    def vailid_moves(cost: int, pos: Vec, vel: Vec) -> Iterator[tuple[Vec, Vec, int]]:
        for pos, vel, extra_cost in moves(pos, vel):
            total_cost = cost + extra_cost
            if total_cost < costs[(pos, vel)] and pos not in walls:
                yield pos, vel, total_cost

    heappush(queue, (0, start, EAST))
    costs[(start, EAST)] = 0

    while queue:
        for pos, vel, cost in vailid_moves(*heappop(queue)):
            costs[(pos, vel)] = cost
            heappush(queue, (cost, pos, vel))

    return costs


def best_tiles(costs: Mapping[State, int], end_states: set[State]) -> int:
    to_visit = end_states
    visited = {pos for pos, _ in end_states}

    def backtrack_moves(pos: Vec, vel: Vec) -> Iterator[State]:
        for prev_pos, prev_vel, move_cost in moves(pos, vel, direction=-1):
            if costs[(prev_pos, prev_vel)] + move_cost == costs[(pos, vel)]:
                yield prev_pos, prev_vel

    while to_visit:
        for pos, vel in backtrack_moves(*to_visit.pop()):
            visited.add(pos)
            to_visit.add((pos, vel))

    return visited


if __name__ == "__main__":
    data = open("data.in").read().splitlines()
    walls, start, end = parse_grid(data)

    # Part 1
    costs = explore_maze(walls, start)
    cheapest = min(costs[(end, dir)] for dir in DIRS)
    print(cheapest)

    # Part 2
    end_states = {(end, dir) for dir in DIRS if costs[(end, dir)] == cheapest}
    print(len(best_tiles(costs, end_states)))
