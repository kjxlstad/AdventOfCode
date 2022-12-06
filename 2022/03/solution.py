import string


def compartments(rucksacks):
    return [
        (sack[: len(sack) // 2], sack[len(sack) // 2 :]) for sack in rucksacks
    ]


def groups(rucksacks):
    return [
        [sack for sack in rucksacks[i : i + 3]]
        for i in range(0, len(rucksacks), 3)
    ]


def duplicates(badges):
    return [
        next(iter(set.intersection(*[set(s) for s in subset])))
        for subset in badges
    ]


def type_sum(badges):
    return sum(string.ascii_letters.index(badge) + 1 for badge in badges)


if __name__ == "__main__":
    with open("data.in", "r") as f:
        rucksacks = f.read().strip().split("\n")

    # Part 1
    print(type_sum(duplicates(compartments(rucksacks))))

    # Part 2
    print(type_sum(duplicates(groups(rucksacks))))
