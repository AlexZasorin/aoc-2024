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


def is_mostly_increasing(levels: list[int]) -> bool:
    inc = 0
    dec = 0

    for i, level in enumerate(levels):
        if i == 0:
            continue
        if level > levels[i - 1]:
            inc += 1
        elif level < levels[i - 1]:
            dec += 1

    return inc > dec


def is_safe_recursive(
    levels: list[int], increasing: bool, prev_level_idx: int, idx: int, threshold: int
) -> bool:
    if idx >= len(levels):
        return True

    if (levels[idx] < levels[prev_level_idx] and increasing) or (
        levels[idx] > levels[prev_level_idx] and not increasing
    ):
        if threshold <= 0:
            return False
        elif prev_level_idx == 0:
            return is_safe_recursive(
                levels, increasing, prev_level_idx, idx + 1, threshold - 1
            ) or is_safe_recursive(levels, increasing, idx, idx + 1, threshold - 1)
        else:
            return is_safe_recursive(
                levels, increasing, prev_level_idx, idx + 1, threshold - 1
            ) or is_safe_recursive(
                levels, increasing, prev_level_idx - 1, idx, threshold - 1
            )

    diff = abs(levels[idx] - levels[prev_level_idx])
    if diff < 1 or diff > 3:
        if threshold <= 0:
            return False
        elif prev_level_idx == 0:
            return is_safe_recursive(
                levels, increasing, prev_level_idx, idx + 1, threshold - 1
            ) or is_safe_recursive(levels, increasing, idx, idx + 1, threshold - 1)
        else:
            return is_safe_recursive(
                levels, increasing, prev_level_idx, idx + 1, threshold - 1
            ) or is_safe_recursive(
                levels, increasing, prev_level_idx - 1, idx, threshold - 1
            )

    return is_safe_recursive(levels, increasing, idx, idx + 1, threshold)


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

    safe = 0
    for line in input:
        levels: list[int] = list(map(lambda x: int(x), line.split(" ")))
        if is_safe_recursive(levels, is_mostly_increasing(levels), 0, 1, 1):
            safe += 1

    return safe


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        lines = file.readlines()

    print(part1(lines))
    print(part2(lines))
