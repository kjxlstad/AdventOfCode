from functools import cmp_to_key

RANKS = "23456789TJQKA"
JOKER_RANKS = "J23456789TQKA"

PAIR_TYPES = [[5], [4], [3, 2], [3], [2, 2], [2], [1]]


def parse_hand(line):
    cards, bid = line.split()
    return cards, int(bid)


def n_of_a_kind(cards, n):
    return next((s for s in set(cards) if cards.count(s) == n), False)


def ns_of_kinds(cards, ns):
    match ns:
        case []: return True
        case [n, *ns]:
            # if there is a pair, remove it and check for the rest
            pair_rank = n_of_a_kind(cards, n)
            return pair_rank and ns_of_kinds(cards.replace(pair_rank, ""), ns)


def pair_strength(cards, joker):
    if joker and cards != "JJJJJ":
        most_frequent_rank = max(set(cards) - {"J"}, key=cards.count)
        cards = cards.replace("J", most_frequent_rank)
    return next(i for i, t in enumerate(PAIR_TYPES) if ns_of_kinds(cards, t))


def compare(a, b, joker):
    if (diff := pair_strength(a, joker) - pair_strength(b, joker)) != 0:
        # care since pair_types are in descending order
        return -diff

    ranks = JOKER_RANKS if joker else RANKS
    for card_a, card_b in zip(a, b):
        if (diff := ranks.index(card_a) - ranks.index(card_b)) != 0:
            return diff

    return 0


def total_winnings(hands, joker=False):
    key_func = cmp_to_key(lambda a, b: compare(a[0], b[0], joker))
    in_order = sorted(hands, key=key_func)
    return sum(bid * i for i, (_, bid) in enumerate(in_order, start=1))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        content = f.read()

    hands = [parse_hand(line) for line in content.split("\n")]

    # Part 1
    print(total_winnings(hands))

    # Part 2
    print(total_winnings(hands, joker=True))
