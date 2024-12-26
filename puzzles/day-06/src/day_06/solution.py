from enum import Enum
from typing import Final

from aoc_2024.vector import Vector


class Direction(Enum):
    NORTH = Vector(-1, 0)
    EAST = Vector(0, 1)
    SOUTH = Vector(1, 0)
    WEST = Vector(0, -1)


class Tile(Enum):
    GUARD_NORTH = "^"
    GUARD_EAST = ">"
    GUARD_SOUTH = "v"
    GUARD_WEST = "<"
    OBSTACLE = "#"
    EMPTY = "."


class Guard:
    pos: Vector
    dir: Direction

    def __init__(self, pos: Vector, dir: Direction) -> None:
        self.pos = pos
        self.dir = dir

    def turn_right(self):
        match self.dir:
            case Direction.NORTH:
                self.dir = Direction.EAST
            case Direction.EAST:
                self.dir = Direction.SOUTH
            case Direction.SOUTH:
                self.dir = Direction.WEST
            case Direction.WEST:
                self.dir = Direction.NORTH

    def next_step(self):
        return self.pos + self.dir.value

    def step(self):
        self.pos += self.dir.value


class Grid:
    board: list[list[str]]

    def __init__(self, board: list[list[str]]) -> None:
        self.board = board

    @property
    def x(self):
        return len(self.board)

    @property
    def y(self):
        return len(self.board[0])

    def at(self, x: int, y: int) -> str:
        return self.board[x][y]

    def in_bounds(self, pos: Vector):
        return pos.x >= 0 and pos.x < self.x and pos.y >= 0 and pos.y < self.y

    def __iter__(self):
        return iter(self.board)

    def __len__(self):
        return len(self.board)


def find_guard(board: Grid) -> Vector:
    for x, row in enumerate(board):
        for y, item in enumerate(row):
            if item == Tile.GUARD_NORTH.value:
                return Vector(x, y)

    # This condition will never be reached in our input value, I just don't want to type this as returning Position | None
    return Vector(0, 0)


def in_bounds(pos: Vector, x: int, y: int):
    return pos.x >= 0 and pos.x < x and pos.y >= 0 and pos.y < y


def turn_right(dir: Direction) -> Direction:
    if dir == Direction.NORTH:
        return Direction.EAST
    elif dir == Direction.EAST:
        return Direction.SOUTH
    elif dir == Direction.SOUTH:
        return Direction.WEST
    else:
        return Direction.NORTH


def part1(board: list[list[str]]):
    grid = Grid(board)
    init_pos: Final[Vector] = find_guard(grid)
    guard = Guard(init_pos, Direction.NORTH)

    visited: set[Vector] = set([guard.pos])
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step()
        if grid.at(next_step.x, next_step.y) == Tile.OBSTACLE.value:
            guard.turn_right()
            guard.step()

            if grid.in_bounds(guard.pos):
                visited.add(guard.pos)
        else:
            guard.step()
            if in_bounds(guard.pos, grid.x, grid.y):
                visited.add(guard.pos)

    return len(visited)


def part2(board: Grid):
    pass
