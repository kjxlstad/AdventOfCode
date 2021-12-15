from itertools import repeat
import heapq


def cost(grid, x, y):
    i, j = x // 100, y // 100
    x, y = x % 100, y % 100

    return (grid[y][x] + i + j - 1) % 9 + 1


def neighbors(grid, x, y, bounds):
    xs = set(zip(range(max(0, x - 1), min(bounds[0], x + 2)), repeat(y)))
    ys = set(zip(repeat(x), range(max(0, y - 1), min(bounds[1], y + 2))))

    return {(i, j): cost(grid, i, j) for i, j in (xs | ys) - {(x, y)}}


def dijkstra(grid, source, target):
    total_risk = {}
    heap = [(*source, grid[source[1]][source[0]])]

    bounds = (target[0] + 1, target[1] + 1)

    while heap:
        x, y, cost = heapq.heappop(heap)

        if (x, y) == target:
            return cost

        for pos, risk in neighbors(grid, x, y, bounds).items():
            current_risk = cost + risk
            if total_risk.get(pos, float("inf")) <= current_risk:
                continue
            total_risk[pos] = current_risk
            heapq.heappush(heap, (*pos, current_risk))


def minimum_risk(grid, source=(0, 0), target=(99, 99)):
    return dijkstra(grid, source, target) - grid[source[1]][source[0]]


if __name__ == "__main__":
    grid = [
        [int(cell) for cell in line.strip()] for line in open("data.in", "r").readlines()
    ]

    print(minimum_risk(grid, target=(99, 99)))
    print(minimum_risk(grid, target=(499, 499)))
