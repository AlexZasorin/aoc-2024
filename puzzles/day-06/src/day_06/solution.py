from enum import Enum
from typing import Final

from aoc_2024.measure import measure
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

    def place(self, pos: Vector, tile: Tile):
        self.board[pos.x][pos.y] = tile.value

    def at(self, x: int, y: int) -> str:
        return self.board[x][y]

    def in_bounds(self, pos: Vector):
        return pos.x >= 0 and pos.x < self.x and pos.y >= 0 and pos.y < self.y

    def __iter__(self):
        return iter(self.board)

    def __len__(self):
        return len(self.board)


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

    def next_step(self, grid: Grid) -> Vector:
        next_step = self.pos + self.dir.value
        while (
            grid.in_bounds(next_step)
            and grid.at(next_step.x, next_step.y) == Tile.OBSTACLE.value
        ):
            self.turn_right()
            next_step = self.pos + self.dir.value

        return next_step

    def step(self, grid: Grid):
        next_step = self.pos + self.dir.value
        while (
            grid.in_bounds(next_step)
            and grid.at(next_step.x, next_step.y) == Tile.OBSTACLE.value
        ):
            self.turn_right()
            next_step = self.pos + self.dir.value

        self.pos = next_step


def find_guard(board: Grid) -> Vector:
    for x, row in enumerate(board):
        for y, item in enumerate(row):
            if item == Tile.GUARD_NORTH.value:
                return Vector(x, y)

    # This condition will never be reached in our input value, I just don't want to type this as returning Position | None
    return Vector(0, 0)


@measure
def part1(board: list[list[str]]):
    grid = Grid(board)
    init_pos: Final[Vector] = find_guard(grid)
    guard = Guard(init_pos, Direction.NORTH)

    visited: set[Vector] = set([guard.pos])
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step(grid)
        if grid.at(next_step.x, next_step.y) == Tile.OBSTACLE.value:
            guard.turn_right()

        guard.step(grid)
        if grid.in_bounds(guard.pos):
            visited.add(guard.pos)

    return len(visited)


def will_it_loop(grid: Grid, guard_pos: Vector, guard_dir: Direction) -> bool:
    slow_guard = Guard(guard_pos, guard_dir)
    fast_guard = Guard(guard_pos, guard_dir)
    while grid.in_bounds(slow_guard.pos) and grid.in_bounds(fast_guard.pos):
        slow_guard.step(grid)
        fast_guard.step(grid)
        fast_guard.step(grid)

        if slow_guard.pos == fast_guard.pos and slow_guard.dir == fast_guard.dir:
            return True

    return False


@measure
def part2(board: list[list[str]]):
    grid = Grid(board)
    init_pos: Final[Vector] = find_guard(grid)
    guard = Guard(init_pos, Direction.NORTH)

    placed: set[Vector] = set()
    loops = 0
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step(grid)

        if next_step not in placed:
            grid.place(next_step, Tile.OBSTACLE)
            loops += 1 if will_it_loop(grid, guard.pos, guard.dir) else 0
            grid.place(next_step, Tile.EMPTY)
            placed.add(next_step)

        guard.step(grid)

    return loops
