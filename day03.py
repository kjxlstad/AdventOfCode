from functools import reduce

data = [
    [int(bit) for bit in line.strip()]
    for line in open("data/day03.in", "r").readlines()
]

# Part 1
def most_common(col):
    return int(sum(col) >= len(col) / 2)


def least_common(col):
    most_common_bit = most_common(col)
    return most_common_bit ^ 1


def bits_to_int(bits):
    return reduce(lambda a, b: (a << 1) + b, bits)


gamma_rate = bits_to_int(map(most_common, zip(*data)))
epsilon_rate = bits_to_int(map(least_common, zip(*data)))

print(gamma_rate * epsilon_rate)


# Part 2
def red(data, criterion, n=0):
    if len(data) == 1:
        return data[0]

    column = list(zip(*data))[n]
    candidates = list(filter(lambda b: b[n] == criterion(column), data))

    return red(candidates, criterion, n + 1)


oxygen_rating = bits_to_int(red(data, most_common))
co2_rating = bits_to_int(red(data, least_common))

print(oxygen_rating * co2_rating)
