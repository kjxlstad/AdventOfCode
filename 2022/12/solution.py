from collections import deque


def find(heightmap, char):
    return [
        (x, y)
        for y, row in enumerate(heightmap)
        for x, c in enumerate(row)
        if c == char
    ]


def elevation(heightmap, x, y):
    char = heightmap[y][x]
    return ord({"S": "a", "E": "z"}.get(char, char))


def neighbors(heightmap, x, y):
    w, h = len(heightmap[0]), len(heightmap)
    all_neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    current_elevation = elevation(heightmap, x, y)

    yield from (
        (x, y)
        for x, y in all_neighbors
        if 0 <= x < w
        and 0 <= y < h
        and elevation(heightmap, x, y) - current_elevation <= 1
    )


def shortest_climb(heightmap, start_points, end):
    visited = set()
    queue = deque([(x, y, 0) for x, y in start_points])

    while queue:
        x, y, steps = queue.popleft()

        if (x, y) == end: return steps
        if (x, y) in visited: continue
        visited.add((x, y))

        for x, y in neighbors(heightmap, x, y):
            queue.append((x, y, steps + 1))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        topography = [list(line.strip()) for line in f]

    target = find(topography, "E")[0]

    # Part 1
    start_pos = find(topography, "S")
    print(shortest_climb(topography, start_pos, target))

    # Part 2
    start_positions = start_pos + find(topography, "a")
    print(shortest_climb(topography, start_positions, target))
