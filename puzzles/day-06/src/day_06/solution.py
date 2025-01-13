from enum import auto, Enum
from typing import Final, TypedDict

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


def visualize_grid(grid_size: Vector, elements: Elements, cell_size: int = 20):
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
        if len(directions) == 1:
            symbol = "^>v<"[list(Direction).index(directions[0])]
        else:
            symbol = "✧"
        draw.text(
            (pos.y * cell_size + cell_size // 2, pos.x * cell_size + cell_size // 2),
            symbol,
            fill="yellow",
            font=ImageFont.truetype(
                "/nix/store/9wbbyajnnrbkvi9azz62wjp6hym4zh4p-jetbrains-mono-2.304/share/fonts/truetype/NerdFonts/JetBrainsMono/JetBrainsMonoNerdFontMono-Regular.ttf",
                12,
            ),
            anchor="mm",
        )
    # Draw guard position

    # Draw grid
    for i in range(grid_size.x + 1):
        draw.line(
            [(0, i * cell_size), (grid_size.y * cell_size, i * cell_size)],
            fill="gray",
            width=1,
        )

    for i in range(grid_size.y + 1):
        draw.line(
            [(i * cell_size, 0), (i * cell_size, grid_size.x * cell_size)],
            fill="gray",
            width=1,
        )
    grid.save("puzzles/day-06/src/day_06/images/grid.png")


# def visualize_grid(grid_size: int, elements: Elements):
#     _, ax = plt.subplots(figsize=(10, 10))
#
#     # Draw grid
#     for i in range(grid_size + 1):
#         _ = ax.axhline(i * 3, color="gray", linewidth=0.5)
#         _ = ax.axvline(i * 3, color="gray", linewidth=0.5)
#
#     # Dictionary for direction arrows and combined symbols
#     direction_symbols = {
#         Direction.NORTH: "↑",
#         Direction.SOUTH: "↓",
#         Direction.WEST: "←",
#         Direction.EAST: "→",
#     }
#
#     # Common direction combinations
#     combined_symbols = {
#         frozenset([Direction.NORTH, Direction.SOUTH]): "↕",
#         frozenset([Direction.WEST, Direction.EAST]): "↔",
#         frozenset([Direction.NORTH, Direction.EAST]): "↗",
#         frozenset([Direction.NORTH, Direction.WEST]): "↖",
#         frozenset([Direction.SOUTH, Direction.EAST]): "↘",
#         frozenset([Direction.SOUTH, Direction.WEST]): "↙",
#         frozenset(
#             [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
#         ): "✧",  # star for all directions
#         frozenset([Direction.NORTH, Direction.SOUTH, Direction.EAST]): "⊢",
#         frozenset([Direction.NORTH, Direction.SOUTH, Direction.WEST]): "⊣",
#         frozenset([Direction.NORTH, Direction.WEST, Direction.EAST]): "⊥",
#         frozenset([Direction.SOUTH, Direction.WEST, Direction.EAST]): "⊤",
#     }
#
#     # Plot elements
#     guard_pos = elements["guard_pos"]
#     _ = ax.text(
#         guard_pos.x + 0.5,
#         guard_pos.x + 0.5,
#         "👮",
#         ha="center",
#         va="center",
#         fontsize=12,
#     )
#
#     for obstacle_pos in elements["obstacles"]:
#         _ = ax.text(
#             obstacle_pos.y + 0.5,
#             obstacle_pos.x + 0.5,
#             "⬛",
#             ha="center",
#             va="center",
#             fontsize=12,
#         )
#
#     for path_pos in elements["original_path"]:
#         _ = ax.add_patch(
#             patches.Rectangle(
#                 (path_pos.x, path_pos.x), 1, 1, facecolor="yellow", alpha=0.3
#             )
#         )
#
#     # Create a dictionary to collect all directions for each position
#     traversed_positions: dict[Vector, set[Direction]] = {}
#     for pos, directions in elements["traversed"]:
#         if pos not in traversed_positions:
#             traversed_positions[pos] = set()
#         for direction in directions:
#             traversed_positions[pos].add(direction)
#
#     # Plot traversed positions with combined symbols
#     for pos, directions in traversed_positions.items():
#         frozen_dirs = frozenset(directions)
#         if len(directions) == 1:
#             # Single direction
#             symbol = direction_symbols[list(directions)[0]]
#         elif frozen_dirs in combined_symbols:
#             # Known combination
#             symbol = combined_symbols[frozen_dirs]
#         else:
#             # Fall back to overlapping arrows for unknown combinations
#             symbol = "+".join(direction_symbols[d] for d in directions)
#
#         _ = ax.text(
#             pos.y + 0.5,
#             pos.x + 0.5,
#             symbol,
#             ha="center",
#             va="center",
#             color="blue",
#             fontsize=12,
#             fontdict={"fontname": "JetBrains Mono"},
#         )
#
#     # Set grid properties
#     _ = ax.set_xlim(0, grid_size)
#     _ = ax.set_ylim(0, grid_size)
#     ax.invert_yaxis()
#     ax.set_aspect("equal")
#
#     plt.savefig("grid.png")


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


def will_it_loop(
    grid: Grid,
    guard_pos: Vector,
    guard_dir: Direction,
    original_path: Visited,
    will_loop: Visited,
    off_grid: Visited,
) -> tuple[Visited, Destination, bool]:
    guard = Guard(guard_pos, guard_dir)
    visited: Visited = set()

    intersects: bool = False
    while grid.in_bounds(guard.pos):
        guard.step(grid)

        if (guard.pos, guard.dir) in original_path:
            intersects = True

        if (guard.pos, guard.dir) in off_grid:
            return visited, Destination.OFF_THE_GRID, intersects

        if (guard.pos, guard.dir) in will_loop:
            return visited, Destination.LOOP, intersects

        if (guard.pos, guard.dir) in visited:
            return visited, Destination.LOOP, intersects

        if grid.in_bounds(guard.pos):
            visited.add((guard.pos, guard.dir))

    return visited, Destination.OFF_THE_GRID, intersects


@measure
def part2(board: list[list[str]]):
    grid = Grid(board)
    init_pos: Final[Vector] = find_guard(grid)
    guard = Guard(init_pos, Direction.NORTH)

    placed: set[Vector] = set()
    original_path: Visited = set([(guard.pos, guard.dir)])
    will_loop: Visited = set()
    off_grid: Visited = set()

    loops = 0
    while grid.in_bounds(guard.pos):
        next_step = guard.next_step(grid)

        if next_step not in placed:
            grid.place(next_step, Tile.OBSTACLE)

            visited, dest, intersects = will_it_loop(
                grid, guard.pos, guard.dir, original_path, will_loop, off_grid
            )

            if dest is Destination.LOOP:
                loops += 1
                if intersects:
                    will_loop |= visited
            elif not intersects:
                off_grid |= visited

            grid.place(next_step, Tile.EMPTY)
            placed.add(next_step)

        guard.step(grid)
        original_path.add((guard.pos, guard.dir))

        obstacles = [
            Vector(x, y)
            for x, row in enumerate(grid)
            for y, item in enumerate(row)
            if item == Tile.OBSTACLE.value
        ]
        # Reduce the will_loop and off_grid sets to one set that contains tuples of position and list of directions
        # Where entries that share the same position are combined
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
        visualize_grid(
            Vector(grid.y, grid.x),
            {
                "guard_pos": guard.pos,
                "obstacles": obstacles,
                "original_path": [pos for pos, _ in original_path],
                "traversed": traversed,
            },
        )
        return 1

    return loops
