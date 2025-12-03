from itertools import chain


def parse_range(line: str) -> range:
    start_str, end_str = map(int, line.split("-"))
    return range(start_str, end_str + 1)


def is_invalid(id_num: str, num_parts: int = 2) -> bool:
    return id_num == id_num[: len(id_num) // num_parts] * num_parts


def is_silly_invalid(id_num: str) -> bool:
    n = len(id_num)
    return any(is_invalid(id_num, num_parts=n // size) for size in range(1, n // 2 + 1))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        ranges = (parse_range(line) for line in f.read().split(","))
        ids = list(chain.from_iterable(ranges))

    # Part 1
    print(sum(n for n in ids if is_invalid(str(n))))

    # Part 2
    print(sum(n for n in ids if is_silly_invalid(str(n))))
