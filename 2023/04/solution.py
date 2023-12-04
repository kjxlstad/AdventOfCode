def parse_line(line):
    _, nums = line.split(":")
    winning, nums = ({int(n) for n in ns.split()} for ns in nums.split("|"))
    return winning, nums


def score(wins):
    return 2 ** (wins - 1) if wins > 0 else 0


def num_scratchcards(wins):
    copies = [1 for _ in wins]

    for i, w in enumerate(wins):
        for j in range(i + 1, i + w + 1):
            copies[j] += copies[i]

    return sum(copies)


with open("data.in", "r") as f:
    lines = f.read().strip("\n").split("\n")
    cards = [parse_line(line) for line in lines]

    wins = [sum(1 for n in picks if n in winning) for winning, picks in cards]

    # Part 1
    print(sum(score(w) for w in wins))

    # Part 2
    print(num_scratchcards(wins))
