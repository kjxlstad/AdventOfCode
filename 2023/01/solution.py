from functools import reduce
from string import ascii_lowercase

SPELLING = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3",
    "four": "4",
    "five": "5e",
    "six": "6",
    "seven": "7",
    "eight": "e8",
    "nine": "n9",
}


def outer_concat(line):
    line = line.strip(ascii_lowercase)
    return int(line[0] + line[-1])


def replace_spelling(line):
    return reduce(lambda line, kv: line.replace(*kv), SPELLING.items(), line)


if __name__ == "__main__":
    with open("data.in", "r") as calibration_document:
        lines = calibration_document.read().split("\n")

    # Part 1
    print(sum(outer_concat(line) for line in lines))

    # Part 2
    print(sum(outer_concat(line) for line in map(replace_spelling, lines)))
