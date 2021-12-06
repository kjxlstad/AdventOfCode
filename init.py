from argparse import ArgumentParser
import requests
from os import path, makedirs
from markdownify import markdownify
import re


def fetch_session_id():
    with open("config", "r") as f:
        return f.read()


def write_problem(url, folder):
    response = requests.get(url)
    response.raise_for_status()

    content = re.findall(r"<main>([\S\s]*?)</main>", response.text)[0].split("\n")

    problem = markdownify("\n".join(content[2:-3]))

    with open(path.join(folder, "problem.md"), "w") as f:
        f.write(problem)


def write_input(url, session_id, folder):
    response = requests.get(f"{url}/input", cookies={"session": session_id})
    response.raise_for_status()

    with open(path.join(folder, "data.in"), "w") as f:
        f.write(response.text)


def touch_solution(folder):
    with open(path.join(folder, "solution.py"), "a+") as f:
        f.write("")


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("day", type=int)
    return parser.parse_args().day


if __name__ == "__main__":
    day = parse_args()

    url = f"https://adventofcode.com/2021/day/{day}"
    folder = f"day{day:02d}"

    session = fetch_session_id()

    if not path.isdir(folder):
        makedirs(folder)
        write_problem(url, folder)
        write_input(url, session, folder)
        touch_solution(folder)
