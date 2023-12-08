from functools import reduce
from operator import mul
from math import ceil, floor, ulp, sqrt


def parse_line(line, ignore_spaces):
    _, *nums = line.split()
    if ignore_spaces:
        nums = ["".join(nums)]
    return [int(n) for n in nums]


def parse_poster(poster, ignore_spaces=False):
    lines = poster.split("\n")
    return list(zip(*map(lambda l: parse_line(l, ignore_spaces), lines)))


def distance_traveled(total_time, button_time):
    travel_time = total_time - button_time
    velocity = button_time
    return velocity * travel_time


def num_records(time, current_record):
    return sum(
        1
        for button_time in range(time - 1)
        if distance_traveled(time, button_time) > current_record
    )


def quadratic_formula(a, b, c):
    disriminant = sqrt(b**2 - 4 * a * c)

    return ((-b + disriminant) / (2 * a), (-b - disriminant) / (2 * a))


def num_records_fast(time, record):
    # number of new records is equal to the number of whole number solutions
    # to the inequality x(t - x) > d, where x is the button press time.
    # Solve for roots of the quadratic equation -x^2 + tx - d = 0
    root_0, root_1 = quadratic_formula(-1, time, -record)

    # Add epsilon to ignore whole numbered roots
    epsilon = ulp(0)
    return floor(root_1 - epsilon) - ceil(root_0 + epsilon) + 1


if __name__ == "__main__":
    with open("data.in", "r") as content:
        poster = content.read()

    # Part 1
    races = parse_poster(poster)
    print(reduce(mul, (num_records(time, record) for time, record in races)))

    # Part 2
    [(time, record)] = parse_poster(poster, ignore_spaces=True)
    print(num_records_fast(time, record))
