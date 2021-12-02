from operator import lt

sweeps = tuple(map(int, open("data/day1.in", "r").readlines()))


# Part 1
def count_increasing(it):
    return sum(map(lt, it[:-1], it[1:]))


print(count_increasing(sweeps))

# Part 2
triplets = tuple(map(sum, zip(sweeps, sweeps[1:], sweeps[2:])))
print(count_increasing(triplets))
