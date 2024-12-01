def parse_line(line: str) -> tuple[int, int]:
    left, right = line.split("   ")
    return int(left), int(right)


if __name__ == "__main__":
    lines = open("data.in").read().splitlines()
    left, right = zip(*map(parse_line, lines))

    # Part 1
    pairs = zip(sorted(left), sorted(right))
    dists = (abs(l - r) for l, r in pairs)
    print(sum(dists))

    # Part 2
    similarity = [l * right.count(l) for l in left]
    print(sum(similarity))
