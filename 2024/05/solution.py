from functools import cmp_to_key, partial
from itertools import pairwise
from typing import Callable


def split_ints(text: str, delim: str) -> list[int]:
    return [int(num) for num in text.split(delim)]


def middle_num(nums: list[int]) -> int:
    return nums[len(nums) // 2]


def is_ordered(pages: list[int], rules: list[tuple[int, int]]) -> bool:
    return not any((b, a) in rules for a, b in pairwise(pages))


def page_key(rules: list[tuple[int, int]]) -> Callable[[int], int]:
    return cmp_to_key(lambda a, b: -1 if (a, b) in rules else 1)


if __name__ == "__main__":
    rules, pages = open("data.in").read().split("\n\n")
    rules = [tuple(split_ints(rule, "|")) for rule in rules.split("\n")]
    pages = [split_ints(page, ",") for page in pages.split("\n")]

    # Part 1
    ordered = partial(is_ordered, rules=rules)
    print(sum(middle_num(page) for page in pages if ordered(page)))

    # Part 2
    sort = partial(sorted, key=page_key(rules))
    print(sum(middle_num(sort(page)) for page in pages if not ordered(page)))
