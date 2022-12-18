from itertools import permutations
from functools import reduce
from operator import xor
from collections import deque


def faces(x, y, z):
    return {
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    }


def count(droplets, predicate):
    return sum(
        predicate(face) for droplet in droplets for face in faces(*droplet)
    )


def neighbors(current, droplets, seen):
    return [
        face
        for face in (faces(*current) - droplets - seen)
        if all(-1 <= droplet <= 25 for droplet in face)
    ]


def flood_fill(droplets):
    visited = set()
    queue = deque([(-1, -1, -1)])

    while queue:
        current = queue.pop()
        queue.extend(neighbors(current, droplets, visited))
        visited |= {current}

    return visited


if __name__ == "__main__":
    with open("data.in", "r") as f:
        droplets = {tuple(int(c) for c in line.split(",")) for line in f}

    # Part 1
    print(count(droplets, lambda s: s not in droplets))

    # Part 2
    visited = flood_fill(droplets)
    print(count(droplets, lambda s: s in visited))
