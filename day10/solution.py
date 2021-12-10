from functools import reduce

OPEN = "(", "[", "{", "<"
CLOSE = ")", "]", "}", ">"

PENALTY = dict(zip(CLOSE, (3, 57, 1197, 25137)))


def add(a, b):
    return a + b[0], b[1]


def autocomplete_score(stack):
    return reduce(lambda a, b: a * 5 + OPEN.index(b) + 1, reversed(stack), 0)


def parse(expression, stack="", error=False):
    if not len(expression):
        return 0, 0 if error else autocomplete_score(stack)

    first_char, *rest = expression

    if first_char in OPEN:
        return add(0, parse(rest, stack + first_char, error))

    if (stack[-1], first_char) in zip(OPEN, CLOSE):
        return add(0, parse(rest, stack[:-1], error))

    return add(PENALTY[first_char], parse(rest, stack[:-1], error=True))


if __name__ == "__main__":
    lines = [line.strip() for line in open("data.in", "r").readlines()]

    syntax_scores, autocomplete_scores = zip(
        *(parse(expression) for expression in lines)
    )

    # Part 1
    print(sum(syntax_scores))

    # part 2
    autocomplete_scores = list(filter(None, autocomplete_scores))
    print(sorted(autocomplete_scores)[len(autocomplete_scores) // 2])
