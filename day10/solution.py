from functools import reduce

OPEN = "(", "[", "{", "<"
CLOSE = ")", "]", "}", ">"
PENALTY = dict(zip(CLOSE, (3, 57, 1197, 25137)))


def add(a, b):
    return a + b[0], b[1]


def autocomplete_score(stack, error):
    # Only score autocomplete if expression was error free
    return (
        0 if error else reduce(lambda a, b: a * 5 + OPEN.index(b) + 1, reversed(stack), 0)
    )


def parse(expression, stack="", error=False):
    # Stack depleted, parsing done
    if not len(expression):
        return 0, autocomplete_score(stack, error)

    first_char, *rest = expression

    # Opening char, parse rest with char in stack
    if first_char in OPEN:
        return add(0, parse(rest, stack + first_char, error))

    # Closing char pairs up with last in stack, pop and parse rest
    if (stack[-1], first_char) in zip(OPEN, CLOSE):
        return add(0, parse(rest, stack[:-1], error))

    # Closing char not pairing up, pop, add penalty and parse rest with error
    return add(PENALTY[first_char], parse(rest, stack[:-1], error=True))


if __name__ == "__main__":
    lines = [line.strip() for line in open("data.in", "r").readlines()]

    # Compute scores, remove entires of zero in autocomplete_scores
    syntax_scores, autocomplete_scores = zip(*(parse(expression) for expression in lines))
    autocomplete_scores = list(filter(None, autocomplete_scores))

    # Part 1
    print(sum(syntax_scores))

    # Part 2    
    print(sorted(autocomplete_scores)[len(autocomplete_scores) // 2])
