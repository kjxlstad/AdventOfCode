def next_lit(algo, n, window):
    return sum(1 << (8 - z) for z in range(9) if window(z)) in algo[n % len(algo)]


def window(i, j, image):
    return lambda z: (i - 1 + z % 3, j - 1 + z // 3) in image


def pad(image):
    (x_min, x_max), (y_min, y_max) = ((min(d), max(d)) for d in zip(*image))
    return range(x_min - 1, x_max + 2), range(y_min - 1, y_max + 2)


def enhance(image, algo, n=1):
    if n == 0:
        return len(image)

    x_range, y_range = pad(image)

    enhanced = {
        (i, j)
        for i in x_range
        for j in y_range
        if next_lit(algo, n, window(i, j, image))
    }

    return enhance(enhanced, algo, n - 1)


def parse_algo(algo):
    def alg(state, func=lambda x: x):
        return {func(i) for i, lit in enumerate(algo) if lit == state}

    if algo[0] == "#" and algo[-1] == ".":
        return [alg("."), alg("#", lambda x: x ^ 511)]

    return [alg("#")]


if __name__ == "__main__":
    algo, image = open("data.in", "r").read().split("\n\n")

    image = {
        (i, j)
        for j, line in enumerate(image.split("\n"))
        for i, p in enumerate(line)
        if p == "#"
    }

    algo = parse_algo(algo)

    # Part 1
    print(enhance(image, algo, 2))

    # Part 2
    print(enhance(image, algo, 50))
