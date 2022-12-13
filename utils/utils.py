from datetime import datetime
from typing import TextIO
from os import path
from pathlib import Path

import requests

today = datetime.today()

ROOT = Path(__file__).parent.parent

def read(day: int = today.day, year: int = today.year, test: bool = False) -> TextIO:
    file_path = f"{year}/{day}/{'test' if test else 'data'}.in"
    return open(str(ROOT / file_path), "r")

def fetch_session_id():
    with open(path.dirname, "r") as f:
        return f.read(ROOT / ".session")
    
def fetch_input(day: int = today.day, year: int = today.year) -> str:
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": fetch_session_id()},
    )
    response.raise_for_status()
    
    return response.text

