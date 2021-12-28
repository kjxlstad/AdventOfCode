from functools import cache
from itertools import product


def deterministic_dice():
    side = 1
    while True:
        yield 3 * (side + 1)
        side = (side + 3) % 100


def take_turn(positions, scores=[0, 0], rolls=0, turn=0):
    if max(scores) >= 1000:
        return rolls * min(scores)

    positions[turn] = (positions[turn] + next(roll)) % 10
    scores[turn] += positions[turn] + 1

    return take_turn(positions, scores, rolls + 3, (turn + 1) % 2)


def flip(func, *args):
    args = [arg[::-1] for arg in args]
    return func(*args)[::-1]


@cache
def dirac_dice(positions, scores=(0, 0)):
    won = [score >= 21 for score in scores]
    if True in won:
        return won

    total_wins = (0, 0)

    for rolls in product([1, 2, 3], repeat=3):
        new_positions = (positions[0] + sum(rolls)) % 10, positions[1]
        new_scores = scores[0] + new_positions[0] + 1, scores[1]

        wins = flip(dirac_dice, new_positions, new_scores)
        total_wins = [total + new for total, new in zip(total_wins, wins)]

    return total_wins


if __name__ == "__main__":
    positions = [int(line.split()[-1]) - 1 for line in open("data.in", "r")]

    roll = deterministic_dice()

    # Part 1
    print(take_turn(positions.copy()))

    # Part 2
    print(max(dirac_dice(tuple(positions))))
