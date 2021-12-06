def propagate(fishes):
    # Aging
    aged_fish = {age: fishes[(age + 1) % 9] for age in range(9)}

    # Spawning
    aged_fish[6] += fishes[0]

    return aged_fish


def simulate(fishes, days_left):
    if not days_left:
        return sum(fishes.values())

    return simulate(propagate(fishes), days_left - 1)


if __name__ == "__main__":
    fish = [int(n) for n in open("data.in", "r").read().split(",")]

    fish_ages = {age: fish.count(age) for age in range(9)}

    print(simulate(fish_ages, 80))
    print(simulate(fish_ages, 256))
