from collections import namedtuple
from itertools import combinations, pairwise

Tile = namedtuple("Tile", ["x", "y"])
Rectangle = namedtuple("Rectangle", ["x_min", "y_min", "x_max", "y_max"])


def parse_tile(text: str) -> Tile:
    x, y = map(int, text.split(","))
    return Tile(x, y)


def sort_rectangle(corner_a: Tile, corner_b: Tile) -> Rectangle:
    x_min = min(corner_a.x, corner_b.x)
    x_max = max(corner_a.x, corner_b.x)
    y_min = min(corner_a.y, corner_b.y)
    y_max = max(corner_a.y, corner_b.y)
    return Rectangle(x_min, y_min, x_max, y_max)


def area(rect: Rectangle) -> int:
    width = rect.x_max - rect.x_min + 1
    height = rect.y_max - rect.y_min + 1
    return width * height


def intersects(rect_a: Rectangle, rect_b: Rectangle) -> bool:
    return (
        rect_a.x_min < rect_b.x_max
        and rect_a.y_min < rect_b.y_max
        and rect_a.x_max > rect_b.x_min
        and rect_a.y_max > rect_b.y_min
    )


def is_valid(rect: Rectangle, green_walls: list[Rectangle]) -> bool:
    return not any(intersects(rect, wall) for wall in green_walls)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        red_tiles = [parse_tile(line) for line in f.read().splitlines()]

    rects = sorted(
        (sort_rectangle(a, b) for a, b in combinations(red_tiles, 2)),
        key=area,
        reverse=True,
    )

    # Part 1
    print(area(rects[0]))

    # Part 2
    tile_pairs = pairwise(red_tiles + [red_tiles[0]])
    green_walls = [sort_rectangle(a, b) for a, b in tile_pairs]
    valid_rects = (r for r in rects if is_valid(r, green_walls))
    print(area(next(valid_rects)))
