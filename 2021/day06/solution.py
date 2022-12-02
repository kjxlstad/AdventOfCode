def propagate(fish):
    # Aging
    aged_fish = {age: fish[(age + 1) % 9] for age in range(9)}

    # Spawning
    aged_fish[6] += fish[0]

    return aged_fish


def simulate(fish, days_left):
    if not days_left:
        return sum(fish.values())

    return simulate(propagate(fish), days_left - 1)


if __name__ == "__main__":
    fish = [int(n) for n in open("data.in", "r").read().split(",")]

    fish_ages = {age: fish.count(age) for age in range(9)}

    print(simulate(fish_ages, 80))
    print(simulate(fish_ages, 256))
