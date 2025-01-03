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

    _ = part1(board)
    _ = part2(board)
