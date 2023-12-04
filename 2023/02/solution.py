from itertools import groupby
from functools import reduce
from operator import mul

COLORS = "red", "green", "blue"
CAP = dict(zip(COLORS, (12, 13, 14)))


def parse_cube(cube):
    num, color = cube.strip().split(" ")
    return (color, int(num))


def parse_game(game):
    game_id, num_cubes = game.split(":")
    game_id = int(game_id.split(" ")[1])

    all_cubes = sorted(
        parse_cube(cube)
        for set in num_cubes.split(";")
        for cube in set.split(",")
    )

    num_cubes = {
        color: [num for _, num in cubes]
        for color, cubes in groupby(sorted(all_cubes), lambda cube: cube[0])
    }
    return (game_id, num_cubes)


def possible(game):
    return all(max(nums) <= CAP[color] for color, nums in game.items())


def power(game):
    return reduce(mul, (max(nums) for nums in game.values()))


if __name__ == "__main__":
    with open("data.in", "r") as f:
        games = dict(parse_game(game) for game in f.read().split("\n"))

    # Part 1
    print(sum(game_id for game_id, game in games.items() if possible(game)))

    # Part 2
    print(sum(power(game) for game in games.values()))
