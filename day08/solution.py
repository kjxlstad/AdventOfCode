from functools import reduce

# Lit segments per number, segments following  pin order convention a-g
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
NUMBERS_PER_LENGTH = {
    2: (1,),
    3: (7,),
    4: (4,),
    5: (2, 3, 5),
    6: (0, 6, 9),
    7: (8,),
}


symmetric_diff = lambda sets: set(reduce(lambda p, q: p ^ q, sets))
intersection = lambda sets: set(reduce(lambda p, q: p & q, sets))
union = lambda sets: set(reduce(lambda p, q: p | q, sets))
twice = lambda sets: union(sets) - symmetric_diff(sets)
once = lambda sets: symmetric_diff(sets) - intersection(sets)


def infer_wiring(encoded):
    top = encoded[(7,)][0] - encoded[(1,)][0]
    upper_right = encoded[(1,)][0] - intersection(encoded[(0, 6, 9)])
    lower_right = encoded[(1,)][0] - upper_right
    middle = intersection(encoded[(2, 3, 5)]) & twice(encoded[(0, 6, 9)])
    bottom = intersection(encoded[(2, 3, 5)]) - top - middle
    lower_left = once(encoded[(2, 3, 5)]) - encoded[(4,)][0]
    upper_let = once(encoded[(2, 3, 5)]) & encoded[(4,)][0]

    # Decoded segment for each actual segment
    return top, upper_right, lower_right, bottom, lower_left, upper_let, middle


def decode_number(wiring, number):
    # Calculate the lit segments for each figure
    segments = [
        [int(any(letter in wire for letter in figure)) for wire in wiring]
        for figure in number
    ]

    # Chain together to full number
    return reduce(
        lambda a, b: a * 10 + b,
        (SEGMENTS.index(tuple(segment)) for segment in segments),
    )


def find_correspondences(inputs):
    # Number(s): (list of) corresponding set of segments
    correspondences = {}

    for number in inputs:
        n = NUMBERS_PER_LENGTH[len(number)]
        correspondences[n] = correspondences.get(n, []) + [{*number}]

    return correspondences


def decode_output(line):
    inputs, output = line

    correspondences = find_correspondences(inputs)
    wiring = infer_wiring(correspondences)

    return decode_number(wiring, output)


if __name__ == "__main__":
    # Each line contains [inputs, output]
    lines = [
        [number.split(" ") for number in line.strip().split(" | ")]
        for line in open("data.in", "r").readlines()
    ]

    # Part 1
    print(sum(
        len([figure for figure in output if len(figure) in {2, 3, 4, 7}])
        for _, output in lines
    ))

    # Part 2
    print(sum(decode_output(line) for line in lines))
