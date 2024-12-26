from enum import Enum
from time import perf_counter
from typing import Callable, Final, ParamSpec, TypeVar

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


def format_time(seconds: float) -> tuple[float, str]:
    if seconds < 1e-6:  # Less than 1 microsecond
        return seconds * 1e9, "nanoseconds"
    elif seconds < 1e-3:  # Less than 1 millisecond
        return seconds * 1e6, "microseconds"
    elif seconds < 1:  # Less than 1 second
        return seconds * 1e3, "milliseconds"
    elif seconds < 60:  # Less than 1 minute
        return seconds, "seconds"
    else:
        return seconds / 60, "minutes"


P = ParamSpec("P")
R = TypeVar("R")


def measure(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()

        time_taken = end - start
        value, unit = format_time(time_taken)
        print(f"Output: {result}")
        print(f"Calculated in {value:.2f} {unit}")

        return result

    return wrapper


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


@measure
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
        if in_bounds(guard.pos, grid.x, grid.y):
            visited.add(guard.pos)

    return len(visited)


def will_it_loop(grid: Grid, guard_pos: Vector, guard_dir: Direction) -> bool:
    guard = Guard(guard_pos, guard_dir)
    visited: set[tuple[Vector, Direction]] = set([(guard.pos, guard.dir)])
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step()
        while (
            grid.in_bounds(next_step)
            and grid.at(next_step.x, next_step.y) == Tile.OBSTACLE.value
        ):
            guard.turn_right()
            next_step = guard.next_step()

        guard.step()

        # print(f"Guard: {guard.pos}, {guard.dir}")
        if (guard.pos, guard.dir) in visited:
            return True

        if in_bounds(guard.pos, grid.x, grid.y):
            visited.add((guard.pos, guard.dir))

    return False


@measure
def part2(board: list[list[str]]):
    grid = Grid(board)
    init_pos: Final[Vector] = find_guard(grid)
    guard = Guard(init_pos, Direction.NORTH)

    placed: set[Vector] = set()
    loops = 0
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step()
        while grid.at(next_step.x, next_step.y) == Tile.OBSTACLE.value:
            guard.turn_right()
            next_step = guard.next_step()

        if next_step not in placed:
            grid.place(next_step, Tile.OBSTACLE)
            loops += 1 if will_it_loop(grid, guard.pos, guard.dir) else 0
            grid.place(next_step, Tile.EMPTY)
            placed.add(next_step)

        guard.step()

    return loops
