import sys

from .solution import part1, part2


def main() -> None:
    day_str = sys.argv[0].split("/")[-1]
    print(f"Hello from {day_str}!")

    with open(f"inputs/{day_str}.txt", "r") as file:
        lines = file.readlines()

    board: list[list[str]] = []
    for line in lines:
        board.append([*line])

    result = part1(board)
    print(f"Output: {result}")
    result2 = part2(board)
    print(f"Output: {result2}")
