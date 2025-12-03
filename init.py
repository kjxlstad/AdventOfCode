from argparse import ArgumentParser
from datetime import date
from pathlib import Path

from aocd import get_puzzle  # advent-of-code-data


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--day", type=int, default=date.today().day)
    parser.add_argument("--year", type=int, default=date.today().year)
    return parser.parse_args()


def main():
    args = parse_args()

    puzzle = get_puzzle(year=args.year, day=args.day, block=True)

    puzzle.view()

    puzzle_dir = Path(str(args.year)) / f"{args.day:02d}"
    puzzle_dir.mkdir(parents=True, exist_ok=True)

    puzzle_dir.joinpath("solution.py").touch()
    puzzle_dir.joinpath("data.in").write_text(puzzle.input_data)
    puzzle_dir.joinpath("test.in").write_text(puzzle.examples[0].input_data)


if __name__ == "__main__":
    main()
