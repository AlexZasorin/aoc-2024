import sys

from .solution import part1, part2


def main() -> None:
    day_str = sys.argv[0].split("/")[-1]
    print(day_str)
    print(f"Hello from {day_str}!")
    with open(f"inputs/{day_str}.txt", "r") as file:
        lines = file.readlines()

    print(part1(lines))
    print(part2(lines))
