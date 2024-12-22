import sys

from aoc_2024.vector import Vector

from .solution import Robot, part1, part2


def main() -> None:
    day_str = sys.argv[0].split("/")[-1]
    print(f"Hello from {day_str}!")

    robots: list[Robot] = []
    with open(f"inputs/{day_str}.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            pos_str, vel_str = line.split(" ")
            pos_x, pos_y = pos_str.removeprefix("p=").split(",")
            vel_x, vel_y = vel_str.removeprefix("v=").split(",")

            robots.append(
                Robot(Vector(int(pos_x), int(pos_y)), Vector(int(vel_x), int(vel_y)))
            )

    print(part1(robots))
    part2(robots)
