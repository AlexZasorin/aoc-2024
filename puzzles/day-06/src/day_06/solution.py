from enum import auto, Enum
from typing import Final, TypedDict, override

from PIL import Image, ImageDraw, ImageFont
from aoc_2024.measure import measure
from aoc_2024.vector import Vector

# pyright: reportUnknownMemberType=false


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


class Elements(TypedDict):
    guard_pos: Vector
    obstacles: list[Vector]
    original_path: list[Vector]
    traversed: list[tuple[Vector, list[Direction]]]


def visualize_grid(
    grid_size: Vector, elements: Elements, cell_size: int = 20, frame_num: int = 0
):
    direction_symbols = {
        Direction.NORTH: "↑",
        Direction.SOUTH: "↓",
        Direction.WEST: "←",
        Direction.EAST: "→",
    }

    # Common direction combinations
    combined_symbols = {
        frozenset([Direction.NORTH, Direction.SOUTH]): "↕",
        frozenset([Direction.WEST, Direction.EAST]): "↔",
        frozenset([Direction.NORTH, Direction.EAST]): "↗",
        frozenset([Direction.NORTH, Direction.WEST]): "↖",
        frozenset([Direction.SOUTH, Direction.EAST]): "↘",
        frozenset([Direction.SOUTH, Direction.WEST]): "↙",
        frozenset(
            [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
        ): "*",  # star for all directions
        frozenset([Direction.NORTH, Direction.SOUTH, Direction.EAST]): "⊢",
        frozenset([Direction.NORTH, Direction.SOUTH, Direction.WEST]): "⊣",
        frozenset([Direction.NORTH, Direction.WEST, Direction.EAST]): "⊥",
        frozenset([Direction.SOUTH, Direction.WEST, Direction.EAST]): "⊤",
    }

    # Create a new image
    grid = Image.new(
        "RGBA", (grid_size.y * cell_size, grid_size.x * cell_size), color="black"
    )

    draw = ImageDraw.Draw(grid)
    # Draw obstacles
    for obstacle in elements["obstacles"]:
        draw.rectangle(
            xy=[
                (obstacle.y * cell_size, obstacle.x * cell_size),
                (
                    obstacle.y * cell_size + cell_size - 1,
                    obstacle.x * cell_size + cell_size - 1,
                ),
            ],
            fill="white",
            outline=None,
        )

    # Draw original path
    for path_pos in elements["original_path"]:
        draw.rectangle(
            xy=[
                (path_pos.y * cell_size, path_pos.x * cell_size),
                (
                    path_pos.y * cell_size + cell_size - 1,
                    path_pos.x * cell_size + cell_size - 1,
                ),
            ],
            fill="blue",
            outline=None,
        )
    # Draw traversed positons
    for pos, directions in elements["traversed"]:
        frozen_dirs = frozenset(directions)
        if len(directions) == 1:
            symbol = direction_symbols[list(directions)[0]]
        elif frozen_dirs in combined_symbols:
            symbol = combined_symbols[frozen_dirs]
        else:
            # Fall back to overlapping arrows for unknown combinations
            symbol = "+".join(direction_symbols[d] for d in directions)

        draw.text(
            (pos.y * cell_size + cell_size // 2, pos.x * cell_size + cell_size // 2),
            symbol,
            fill="yellow",
            font=ImageFont.truetype(
                "JetBrainsMonoNerdFont-Regular.ttf",
                24,
            ),
            anchor="mm",
        )

    # Draw guard position
    draw.text(
        (
            elements["guard_pos"].y * cell_size + cell_size // 2,
            elements["guard_pos"].x * cell_size + cell_size // 2,
        ),
        "G",
        font=ImageFont.truetype(
            "JetBrainsMonoNerdFont-Regular.ttf",
            24,
        ),
        anchor="mm",
    )

    # Draw grid
    # for i in range(grid_size.x + 1):
    #     draw.line(
    #         [(0, i * cell_size), (grid_size.y * cell_size, i * cell_size)],
    #         fill="gray",
    #         width=1,
    #     )
    #
    # for i in range(grid_size.y + 1):
    #     draw.line(
    #         [(i * cell_size, 0), (i * cell_size, grid_size.x * cell_size)],
    #         fill="gray",
    #         width=1,
    #     )

    grid.save(f"puzzles/day-06/src/day_06/images/grid-{frame_num}.png")


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


class Destination(Enum):
    OFF_THE_GRID = auto()
    LOOP = auto()


Visited = set[tuple[Vector, Direction]]


class Counter(int):
    value: int = 0

    @override
    def __str__(self):
        return f"{self.value}"


def will_it_loop(
    grid: Grid,
    obstacles: list[Vector],
    guard_pos: Vector,
    guard_dir: Direction,
    original_path: Visited,
    will_loop: Visited,
    off_grid: Visited,
    frames: Counter,
) -> tuple[Visited, Destination, bool]:
    guard = Guard(guard_pos, guard_dir)
    visited: Visited = set()

    obs_start = guard.pos + guard.dir.value
    avoid = set(
        [
            (obs_start + Direction.NORTH.value, Direction.SOUTH),
            (obs_start + Direction.EAST.value, Direction.WEST),
            (obs_start + Direction.SOUTH.value, Direction.NORTH),
            (obs_start + Direction.WEST.value, Direction.EAST),
        ]
    )

    intersects: bool = False
    while grid.in_bounds(guard.pos):
        guard.step(grid)

        if (guard.pos, guard.dir) in original_path or (guard.pos, guard.dir) in avoid:
            intersects = True

        if (guard.pos, guard.dir) in off_grid:
            return visited, Destination.OFF_THE_GRID, intersects

        if (guard.pos, guard.dir) in will_loop:
            return visited, Destination.LOOP, intersects

        if (guard.pos, guard.dir) in visited:
            return visited, Destination.LOOP, intersects

        if grid.in_bounds(guard.pos):
            visited.add((guard.pos, guard.dir))

        ahead = guard.pos + guard.dir.value
        if grid.in_bounds(ahead) and grid.at(ahead.x, ahead.y) == Tile.OBSTACLE.value:
            visualize_grid(
                Vector(grid.y, grid.x),
                visualization_adapter(
                    obstacles, will_loop, off_grid, guard, original_path.union(visited)
                ),
                frame_num=frames,
            )
        frames.value += 1

    return visited, Destination.OFF_THE_GRID, intersects


def visualization_adapter(
    obstacles: list[Vector],
    will_loop: Visited,
    off_grid: Visited,
    guard: Guard,
    original_path: Visited,
) -> Elements:
    traversed_dict: dict[Vector, list[Direction]] = dict()
    for pos, dir in will_loop:
        if pos not in traversed_dict:
            traversed_dict[pos] = [dir]
        else:
            traversed_dict[pos].append(dir)

    for pos, dir in off_grid:
        if pos not in traversed_dict:
            traversed_dict[pos] = [dir]
        else:
            traversed_dict[pos].append(dir)

    traversed = [(pos, dirs) for pos, dirs in traversed_dict.items()]
    return {
        "guard_pos": guard.pos,
        "obstacles": obstacles,
        "original_path": [pos for pos, _ in original_path],
        "traversed": traversed,
    }


# On top of intersection, need to also make sure that it's never interacted with the placed obstacles, must exclude 4 directions around the obstacle


@measure
def part2(board: list[list[str]]):
    grid = Grid(board)

    obstacles = [
        Vector(x, y)
        for x, row in enumerate(grid)
        for y, item in enumerate(row)
        if item == Tile.OBSTACLE.value
    ]

    init_pos: Final[Vector] = find_guard(grid)
    guard = Guard(init_pos, Direction.NORTH)

    placed: set[Vector] = set()
    original_path: Visited = set([(guard.pos, guard.dir)])
    will_loop: Visited = set()
    off_grid: Visited = set()

    loops = 0
    frames = Counter()
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step(grid)

        if next_step not in placed:
            grid.place(next_step, Tile.OBSTACLE)

            visited, dest, intersects = will_it_loop(
                grid=grid,
                obstacles=obstacles,
                guard_pos=guard.pos,
                guard_dir=guard.dir,
                original_path=original_path,
                will_loop=will_loop,
                off_grid=off_grid,
                frames=frames,
            )

            if dest is Destination.LOOP:
                loops += 1
                if not intersects:
                    will_loop |= visited
            elif not intersects:
                off_grid |= visited

            grid.place(next_step, Tile.EMPTY)
            placed.add(next_step)

        guard.step(grid)
        original_path.add((guard.pos, guard.dir))

        visualize_grid(
            Vector(grid.y, grid.x),
            visualization_adapter(obstacles, will_loop, off_grid, guard, original_path),
            frame_num=frames,
        )
        frames.value += 1

    return loops
