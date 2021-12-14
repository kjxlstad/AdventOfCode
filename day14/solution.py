from functools import reduce


def add(acc, pair, count):
    new_pairs = pair[0] + rules[pair], rules[pair] + pair[1]
    return {**acc, **{pair: acc.get(pair, 0) + count for pair in new_pairs}}


def insert(pairs, rules, depth=3):
    if depth == 0:
        return pairs

    new_pairs = reduce(lambda acc, new: add(acc, new[0], new[1]), pairs.items(), {})

    return insert(new_pairs, rules, depth - 1)


def diff(template, pairs):
    unique_elements = set("".join(pairs.keys()))

    def occurrences(element):
        return sum(count for pair, count in pairs.items() if pair[0] == element)

    totals = {element: occurrences(element) for element in unique_elements}

    totals = {**totals, template[-1]: totals.get(template[-1]) + 1}

    return max(totals.values()) - min(totals.values())


if __name__ == "__main__":
    lines = [line.strip() for line in open("data.in", "r").readlines()]
    template, rules = lines[0], lines[2:]

    rules = dict([line.split(" -> ") for line in lines[2:]])

    pairwise = [a + b for a, b in zip(template[:-1], template[1:])]
    pairs = {a: pairwise.count(a) for a in pairwise}

    # Part 1
    print(diff(template, insert(pairs, rules, depth=10)))

    # Part 2
    print(diff(template, insert(pairs, rules, depth=40)))
