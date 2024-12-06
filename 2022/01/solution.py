with open("data.in", "r") as f:
    calories = f.read().strip().split("\n\n")

calories_per_elf = [sum(int(c) for c in group.split("\n")) for group in calories]

# Part 1
print(max(calories_per_elf))

# Part 2
print(sum(sorted(calories_per_elf)[-3:]))
