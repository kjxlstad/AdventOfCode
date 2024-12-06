def parse_data(data):
    balls, *cards = data

    balls = list(map(int, balls.split(",")))

    # Split string into separate bingo cards
    cards = [cards[n + 1 : n + 6] for n in range(0, len(cards), 6)]

    # Split into triple nested list of int
    cards = [
        [[int(n) for n in row.split(" ") if len(n)] for row in card] for card in cards
    ]

    return balls, cards


def has_won(card, balls):
    def bingo(line):
        return all(map(lambda n: n in balls, line))

    lines = [*card, *zip(*card)]

    return any(bingo(line) for line in lines)


def winning_turn(card, balls, turn=0):
    drawn_balls = balls[:turn]

    if has_won(card, drawn_balls):
        return turn

    return winning_turn(card, balls, turn + 1)


def score(card, winning_turn, balls):
    not_picked = [n for row in card for n in row if n not in balls[:winning_turn]]
    return sum(not_picked) * balls[winning_turn - 1]


if __name__ == "__main__":
    # Parse input data into bingo balls and cards
    data = [line.strip() for line in open("data.in", "r").readlines()]
    balls, cards = parse_data(data)

    # Sort cards on winning turn
    cards_won = sorted(
        [(card, winning_turn(card, balls)) for card in cards],
        key=lambda i: i[1],
    )

    # Score first and last winning card
    first, *_, last = cards_won
    print(score(*first, balls), score(*last, balls))
