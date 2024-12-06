def parse(line):
    play, strat = line.split(" ")
    return ord(play) - 65, ord(strat) - 88


def score_conter(play, counter):
    outcome = (play - counter) % 3
    return counter % 3 + 1 + (3, 0, 6)[outcome]


def score_outcome(play, outcome):
    counter = play + (-1, 0, 1)[outcome]
    return counter % 3 + 1 + (0, 3, 6)[outcome]


if __name__ == "__main__":
    with open("data.in", "r") as f:
        guide = f.read().strip().split("\n")

    # Part 1
    print(sum(score_conter(play, counter) for play, counter in map(parse, guide)))

    # Part 2
    print(sum(score_outcome(play, outcome) for play, outcome in map(parse, guide)))
