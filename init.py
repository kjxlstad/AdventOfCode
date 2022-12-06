from argparse import ArgumentParser
import requests
from os import path, makedirs
import re
from datetime import datetime, date
from time import sleep

from markdownify import markdownify

def fetch_session_id():
    with open("config", "r") as f:
        return f.read()


def write_problem(url, folder):
    response = requests.get(url)
    response.raise_for_status()

    content = re.findall(r"<main>([\S\s]*?)</main>", response.text)[0].split(
        "\n"
    )

    problem = markdownify("\n".join(content[2:-3]))

    problem_path = path.join(folder, "problem.md")

    with open(problem_path, "w") as f:
        f.write(problem)

    print(f"Wrote problem description to {problem_path}")


def write_input(url, session_id, folder):
    response = requests.get(f"{url}/input", cookies={"session": session_id})
    response.raise_for_status()

    input_path = path.join(folder, "data.in")

    with open(input_path, "w") as f:
        f.write(response.text)

    print(f"Wrote input file to {input_path}")


def touch_solution(folder):
    solution_path = path.join(folder, "solution.py")

    with open(solution_path, "a+") as f:
        f.write("")

    print(f"Created empty solution in {solution_path}")


def wait_for_opening(n):
    current_time = datetime.now()
    opening_time = current_time.replace(hour=6, minute=0, second=0)
    time_to_opening = (opening_time - current_time).total_seconds()

    if time_to_opening > 0:
        print(f"Problem opens in {time_to_opening} s, waiting for opening")

        sleep(time_to_opening - (n + 1))

        for remaining_seconds in range(n, 0, -1):
            sleep(1)
            print(remaining_seconds)

        print("Go time!")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--year", type=int, default=date.today().year)
    parser.add_argument("--day", type=int, default=date.today().day)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    url = f"https://adventofcode.com/{args.year}/day/{args.day}"
    folder = f"{args.year}/{args.day:02d}"

    session = fetch_session_id()

    wait_for_opening(5)

    if not path.isdir(folder):
        makedirs(folder)
        write_input(url, session, folder)
        touch_solution(folder)

    write_problem(url, folder)
