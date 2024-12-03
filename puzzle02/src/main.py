def is_safe(levels: list[int]) -> bool:
    prev_level = None
    increasing = None
    for level in levels:
        if prev_level is None:
            prev_level = level
        elif level < prev_level:
            if increasing is None:
                increasing = False
            elif increasing is True:
                return False

            diff = abs(level - prev_level)
            if diff < 1 or diff > 3:
                return False

            prev_level = level
        elif level > prev_level:
            if increasing is None:
                increasing = True
            elif increasing is False:
                return False

            diff = abs(level - prev_level)
            if diff < 1 or diff > 3:
                return False

            prev_level = level
        elif level == prev_level:
            return False

    return True


def part1(input: list[str]):
    print("Hello from part1!")

    safe = 0
    for line in input:
        levels: list[int] = list(map(lambda x: int(x), line.split(" ")))
        if is_safe(levels):
            safe += 1

    return safe


def part2(input: list[str]):
    print("Hello from part2!")


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        lines = file.readlines()

    print(part1(lines))
    print(part2(lines))
