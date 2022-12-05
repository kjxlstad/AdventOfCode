def contains(a_min, a_max, b_min, b_max):
    a_in_b = a_min >= b_min and a_max <= b_max
    b_in_a = b_min >= a_min and b_max <= a_max
    return a_in_b or b_in_a


def overlaps(a_min, a_max, b_min, b_max):
    return a_min <= b_max and b_min <= a_max


if __name__ == "__main__":
    with open("data.in", "r") as f:
        pairs = [
            [int(n) for r in pair.split(",") for n in r.split("-")]
            for pair in f.read().splitlines()
        ]

    # Part 1
    print(sum(contains(*pair) for pair in pairs))

    # Part 2
    print(sum(overlaps(*pair) for pair in pairs))
