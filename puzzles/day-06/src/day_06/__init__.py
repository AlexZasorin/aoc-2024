import sys

from .solution import part1, part2


def main() -> None:
    day_str = sys.argv[0].split("/")[-1]
    print(f"Hello from {day_str}!")

    board: list[list[str]] = []
    with open(f"inputs/{day_str}.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            board.append([*line])

    print(part1(board))
    print(part2())
