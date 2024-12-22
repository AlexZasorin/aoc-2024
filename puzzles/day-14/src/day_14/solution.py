from enum import Enum
from functools import reduce
from typing import NamedTuple, override

from aoc_2024.vector import Vector


class Robot(NamedTuple):
    pos: Vector
    vel: Vector


class Tile(Enum):
    GUARD = "x"
    EMPTY = "."


def calculate_position(robot: Robot, steps: int, grid_x: int, grid_y: int) -> Robot:
    pos, vel = robot
    new_x = (pos.x + vel.x * steps) % grid_x
    new_y = (pos.y + vel.y * steps) % grid_y

    return Robot(Vector(new_x, new_y), Vector(vel.x, vel.y))


def sum_quadrants(
    robots: list[Robot], grid_x: int, grid_y: int
) -> tuple[int, int, int, int]:
    mid_x = grid_x // 2
    mid_y = grid_y // 2
    tl, tr, bl, br = 0, 0, 0, 0
    for robot in robots:
        if 0 <= robot.pos.x < mid_x and 0 <= robot.pos.y < mid_y:
            tl += 1
        if 0 <= robot.pos.x < mid_x and mid_y + 1 <= robot.pos.y < grid_y:
            tr += 1
        if mid_x + 1 <= robot.pos.x < grid_x and 0 <= robot.pos.y < mid_y:
            bl += 1
        if mid_x + 1 <= robot.pos.x < grid_x and mid_y + 1 <= robot.pos.y < grid_y:
            br += 1

    return (tl, tr, bl, br)


class BathroomGrid:
    robots: list[Robot]
    dim_x: int
    dim_y: int

    def __init__(self, robots: list[Robot], x: int, y: int):
        self.robots = robots
        self.dim_x = x
        self.dim_y = y

    @override
    def __str__(self) -> str:
        screen: list[list[str]] = [
            list((Tile.EMPTY.value for _ in range(self.dim_x)))
            for _ in range(self.dim_y)
        ]

        for robot in self.robots:
            screen[robot.pos.y][robot.pos.x] = Tile.GUARD.value

        screen_str = ""
        for row in screen:
            screen_str += f"{''.join(row)}\n"

        return screen_str

    def step(self, steps: int):
        updated_robots: list[Robot] = []
        for robot in self.robots:
            updated_robots.append(
                calculate_position(robot, steps, grid_x=101, grid_y=103)
            )

        self.robots = updated_robots


def part1(robots: list[Robot]) -> int:
    dim_x = 101
    dim_y = 103
    bathroom = BathroomGrid(robots, dim_x, dim_y)
    bathroom.step(100)

    quadrants = sum_quadrants(bathroom.robots, grid_x=101, grid_y=103)
    return reduce(lambda x, y: x * y, quadrants)


def move_cursor_up(lines: int):
    print(f"\033[{lines}A", end="")
    print("\033[J", end="")


def part2(robots: list[Robot]) -> None:
    dim_x = 101
    dim_y = 103
    bathroom = BathroomGrid(robots, dim_x, dim_y)
    step = 18

    bathroom.step(18)
    print(f"Current step: {step}")
    print(str(bathroom))
    step += dim_x

    while True:
        command = input()

        if command == "q":
            print("Exitting!")
            break
        elif command == "s":
            bathroom.step(dim_x)
            move_cursor_up(dim_y + 3)
            print(f"Current step: {step}")
            print(str(bathroom))
            step += dim_x
