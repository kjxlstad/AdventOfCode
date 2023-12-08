RANKS = "23456789TJQKA"
JOKER_RANKS = "J23456789TQKA"


def parse_hand(line):
    cards, bid = line.split()
    return cards, int(bid)


def pair_strength(cards, joker):
    if joker and cards != "J" * 5:
        most_frequent = max(set(cards) - {"J"}, key=cards.count)
        cards = cards.replace("J", most_frequent)

    unique_cards = set(cards)
    frequencies = map(cards.count, unique_cards)
    return max(frequencies) - len(unique_cards)


def rank_strength(cards, joker):
    ranks = JOKER_RANKS if joker else RANKS
    return [ranks.index(card) for card in cards]


def strength(cards, joker):
    return (pair_strength(cards, joker), *rank_strength(cards, joker))


def total_winnings(hands, joker=False):
    in_order = sorted(hands, key=lambda hand: strength(hand[0], joker))
    return sum(i * bid for i, (_, bid) in enumerate(in_order, start=1))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        content = f.read()

    hands = [parse_hand(line) for line in content.split("\n")]

    # Part 1
    print(total_winnings(hands))

    # Part 2
    print(total_winnings(hands, joker=True))
