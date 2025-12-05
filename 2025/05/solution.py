from operator import attrgetter


def parse_range(text: str) -> range:
    start, end = map(int, text.split("-"))
    return range(start, end + 1)


def parse_database(text: str) -> tuple[list[range], list[int]]:
    ranges, ingredients = text.split("\n\n")
    return (
        [parse_range(line) for line in ranges.splitlines()],
        [int(line) for line in ingredients.splitlines()],
    )


def is_fresh(ingredient: int, ranges: list[range]) -> bool:
    return any(ingredient in r for r in ranges)


def num_fresh(ranges: list[range]) -> int:
    last_stop = total = 0

    for r in sorted(ranges, key=attrgetter("start")):
        merged = range(max(r.start, last_stop), r.stop)
        last_stop = max(last_stop, r.stop)
        total += len(merged)

    return total


if __name__ == "__main__":
    with open("data.in", "r") as f:
        ranges, ingredients = parse_database(f.read())

    # Part 1
    print(sum(is_fresh(ing, ranges) for ing in ingredients))

    # Part 2
    print(num_fresh(ranges))
