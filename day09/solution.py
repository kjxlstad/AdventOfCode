from functools import reduce


def neighbors(x, y, bounds):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    # Filter out neighbors outside of bounds
    return set(
        filter(lambda pos: all(val in range(*bounds) for val in pos), neighbors)
    )


def low_points(heightmap, bounds):
    # All points in the heightmap with height lower than all neighbors
    return [
        (x, y)
        for y, row in enumerate(heightmap)
        for x, h in enumerate(row)
        if h < min(heightmap[j][i] for i, j in neighbors(x, y, bounds))
    ]


def search_basin(heightmap, x, y, visited=set()):
    # Gather neighbors not visited
    not_visited = neighbors(x, y, (0, 100)) - visited

    # Filter out non-increasing neighbors or neighbors with height 9
    increasing = {
        (i, j) for i, j in not_visited if heightmap[y][x] < heightmap[j][i] < 9
    }

    # Search all neighbors with updated visited list
    searched = [
        search_basin(heightmap, i, j, visited | increasing | {(x, y)})
        for i, j in increasing
    ]

    # Return union of this point and all points in sub search
    return {(x, y)} | reduce(lambda p, q: p | q, searched, set())


if __name__ == "__main__":
    # Read input as square nested list of ints
    heightmap = [
        [int(n) for n in list(line.strip())]
        for line in open("data.in", "r").readlines()
    ]

    bounds = 0, len(heightmap)

    low_points = low_points(heightmap, bounds)

    # Part 1
    print(sum(heightmap[y][x] + 1 for x, y in low_points))

    # Part 2
    basins = [search_basin(heightmap, x, y) for x, y in low_points]
    deepest_basins = sorted(map(len, basins))
    print(reduce(lambda a, b: a * b, deepest_basins[-3:]))
