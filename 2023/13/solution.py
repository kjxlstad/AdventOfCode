def diff(pattern, mirror_pos):
    w, h = len(pattern[0]), len(pattern)
    mirror_len = min(mirror_pos, h - mirror_pos)
    normal_range = range(mirror_pos, mirror_pos + mirror_len)
    mirror_range = range(mirror_pos - 1, mirror_pos - mirror_len - 1, -1)

    return sum(
        pattern[y1][x] != pattern[y2][x]
        for y1, y2 in zip(normal_range, mirror_range)
        for x in range(w)
    )


def mirror_index(pattern, num_smudges):
    indices = range(1, len(pattern))
    mirror_indices = (i for i in indices if diff(pattern, i) == num_smudges)
    return next(mirror_indices, 0)


def transpose(pattern):
    return ["".join(row) for row in zip(*pattern)]


def mirror_summary(pattern, num_smudges=0):
    return (
        100 * mirror_index(pattern, num_smudges)
            + mirror_index(transpose(pattern), num_smudges)
    )


if __name__ == "__main__":
    with open("data.in", "r") as f:
        patterns = [p.split("\n") for p in f.read().split("\n\n")]

    # Part 1
    print(sum(mirror_summary(p) for p in patterns))

    # Part 2
    print(sum(mirror_summary(p, num_smudges=1) for p in patterns))
