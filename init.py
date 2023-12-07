from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import re

from markdownify import markdownify
import requests


def fetch_description(url):
    response = requests.get(url)
    response.raise_for_status()

    content = re.findall(r"<main>([\S\s]*?)</main>", response.text)[0].split(
        "\n"
    )

    problem_desc = markdownify("\n".join(content[2:-3]))
    problem_desc = problem_desc.replace("\n\n", "\n")

    return "# " + problem_desc


def write_description(desc, folder):
    problem_path = folder / "problem.md"

    with open(problem_path, "w") as f:
        f.write(desc)

    print(f"Wrote problem description to {problem_path}")


def write_example(desc, folder):
    # match any content between ticks after a sentence containg "[E/e]xample"
    pattern = r"(?i)example.*?\n```\n(.*?)\n```"

    test_path = folder / "test.in"
    if example := re.search(pattern, desc, re.DOTALL):
        with open(test_path, "w") as f:
            f.write(example.group(1))

        print(f"Wrote example to {test_path}")


def write_input(url, session_id, folder):
    response = requests.get(f"{url}/input", cookies={"session": session_id})
    response.raise_for_status()

    input_path = folder / "data.in"

    with open(input_path, "w") as f:
        f.write(response.text.rstrip("\n"))

    print(f"Wrote input file to {input_path}")


def touch_solution(folder):
    solution_path = folder / "solution.py"

    with open(solution_path, "a+") as f:
        f.write("")

    print(f"Wrote empty solution in {solution_path}")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("day", type=int)
    parser.add_argument("--year", type=int, default=date.today().year)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    url = f"https://adventofcode.com/{args.year}/day/{args.day}"
    folder = Path(f"{args.year}/{args.day:02d}")

    session = open(".session", "r").read().strip()

    desc = fetch_description(url)

    folder.mkdir(exist_ok=True)
    write_input(url, session, folder)
    write_example(desc, folder)
    write_description(desc, folder)

    if not (folder / "solution.py").exists():
        touch_solution(folder)
