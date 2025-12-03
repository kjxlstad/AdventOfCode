from operator import itemgetter


def max_joltage_2(bank: list[int]) -> int:
    first_idx, first = max(enumerate(bank[:-1]), key=itemgetter(1))
    second = max(bank[first_idx + 1 :])
    return first * 10 + second


def max_joltage(bank: list[int], num_batteries: int) -> int:
    if num_batteries == 1:
        return max(bank)

    magnitude = num_batteries - 1
    idx, digit = max(enumerate(bank[:-magnitude]), key=itemgetter(1))
    return digit * 10**magnitude + max_joltage(bank[idx + 1 :], magnitude)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        banks = [[int(b) for b in line.strip()] for line in f.readlines()]

    # Part 1
    print(sum(max_joltage_2(bank) for bank in banks))

    # Part 2
    print(sum(max_joltage(bank, 12) for bank in banks))
