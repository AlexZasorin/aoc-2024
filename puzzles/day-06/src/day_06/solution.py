from enum import Enum
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    NORTH = Position(-1, 0)
    EAST = Position(0, 1)
    SOUTH = Position(1, 0)
    WEST = Position(0, -1)


Board = list[list[str]]


def find_guard(board: Board) -> Position:
    for x, row in enumerate(board):
        for y, item in enumerate(row):
            if item == "^":
                return Position(x, y)

    # This condition will never be reached, I just don't wnat to type this has returning Position | None
    return Position(0, 0)


def in_bounds(pos: Position, x: int, y: int):
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


def part1(board: Board):
    guard_pos = find_guard(board)
    dir = Direction.NORTH
    visited: set[Position] = set([guard_pos])
    while in_bounds(guard_pos, len(board), len(board[0])):
        if board[guard_pos.x + dir.value.x][guard_pos.y + dir.value.y] == "#":
            new_dir = turn_right(dir)

            new_pos = Position(
                guard_pos.x + new_dir.value.x, guard_pos.y + new_dir.value.y
            )
            guard_pos = new_pos
            dir = new_dir
            if in_bounds(new_pos, len(board), len(board[0])):
                visited.add(new_pos)
        else:
            new_pos = Position(guard_pos.x + dir.value.x, guard_pos.y + dir.value.y)
            guard_pos = new_pos
            if in_bounds(new_pos, len(board), len(board[0])):
                visited.add(guard_pos)

    return len(visited)


def part2():
    pass
