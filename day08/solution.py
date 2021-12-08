from functools import reduce

# Code follows standard 7-segment display pin convention a-g
# a: top, b: upper right, c: lower left, d: bottom, e: lower left, f: upper left, g: middle

# Lit segments per number
SEGMENTS = (
    (1, 1, 1, 1, 1, 1, 0),
    (0, 1, 1, 0, 0, 0, 0),
    (1, 1, 0, 1, 1, 0, 1),
    (1, 1, 1, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 1),
    (1, 0, 1, 1, 0, 1, 1),
    (1, 0, 1, 1, 1, 1, 1),
    (1, 1, 1, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 0, 1, 1),
)

# Number of lit elements: corresponding possible displayed numbers
NUMBERS_PER_LENGTH = {2: (1,), 3: (7,), 4: (4,), 5: (2, 3, 5), 6: (0, 6, 9), 7: (8,)}


symmetric_diff = lambda sets: set(reduce(lambda p, q: p ^ q, sets))
intersection = lambda sets: set(reduce(lambda p, q: p & q, sets))
union = lambda sets: set(reduce(lambda p, q: p | q, sets))

# Elements of three sets that appear once and twice
once = lambda sets: symmetric_diff(sets) - intersection(sets)
twice = lambda sets: union(sets) - symmetric_diff(sets)


def infer_wiring(encoded):
    a = encoded[(7,)][0] - encoded[(1,)][0]
    b = encoded[(1,)][0] - intersection(encoded[(0, 6, 9)])
    c = encoded[(1,)][0] - b
    g = intersection(encoded[(2, 3, 5)]) & twice(encoded[(0, 6, 9)])
    d = intersection(encoded[(2, 3, 5)]) - a - g
    e = once(encoded[(2, 3, 5)]) - encoded[(4,)][0]
    f = once(encoded[(2, 3, 5)]) & encoded[(4,)][0]

    # Decoded segment for each actual segment
    return a, b, c, d, e, f, g


def decode_number(wiring, number):
    # Calculate the lit segments for each figure
    segments = [
        [int(any(letter in wire for letter in figure)) for wire in wiring] for figure in number
    ]

    # Chain together to full number
    return reduce(
        lambda a, b: a * 10 + b, (SEGMENTS.index(tuple(segment)) for segment in segments),
    )


def decode_output(line):
    inputs, output = line

    possible_numbers = lambda n: NUMBERS_PER_LENGTH[len(n)]

    # Number(s): (list of) corresponding set of segments
    correspondences = {
        possible_numbers(number): [
            {*n} for n in inputs if possible_numbers(n) == possible_numbers(number)
        ]
        for number in inputs
    }

    wiring = infer_wiring(correspondences)

    return decode_number(wiring, output)


if __name__ == "__main__":
    # Each line contains [inputs, output]
    lines = [
        [number.split(" ") for number in line.strip().split(" | ")]
        for line in open("data.in", "r").readlines()
    ]

    # Part 1
    sum_of_known = sum(
        len([figure for figure in output if len(figure) in {2, 3, 4, 7}]) for _, output in lines
    )
    print(sum_of_known)

    # Part 2
    print(sum(decode_output(line) for line in lines))
