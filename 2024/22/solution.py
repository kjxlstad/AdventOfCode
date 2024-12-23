from collections import defaultdict
from functools import reduce
from itertools import accumulate, pairwise
from operator import add
from typing import Iterable


def evolve(secret: int, modulus: int = 0xFFFFFF + 1) -> int:
    secret ^= (secret * 64) % modulus
    secret ^= (secret // 32) % modulus
    secret ^= (secret * 2048) % modulus
    return secret % modulus


def step(secret: int, num_steps: int = 2000) -> int:
    return reduce(lambda s, _: evolve(s), range(num_steps), secret)


def generate_prices(secret: int, num_steps: int = 2000, modulus: int = 10) -> list[int]:
    secrets = accumulate(range(num_steps), lambda s, _: evolve(s), initial=secret)
    return [s % modulus for s in secrets]


def banana_yield(numbers: list[int], seq_len: int = 4) -> Iterable[int]:
    total_bananas = defaultdict(int)

    for prices in map(generate_prices, numbers):
        seen = set()
        price_changes = [b - a for a, b in pairwise(prices)]
        for i in range(len(prices) - seq_len):
            if (price_change := tuple(price_changes[i : i + seq_len])) not in seen:
                seen |= {price_change}
                total_bananas[price_change] += prices[i + seq_len]

    return total_bananas.values()


if __name__ == "__main__":
    nums = [int(line) for line in open("data.in").read().splitlines()]

    # Part 1
    print(reduce(add, map(step, nums)))

    # Part 2
    print(max(banana_yield(nums)))
