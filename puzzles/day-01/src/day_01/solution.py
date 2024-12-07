from collections import defaultdict


def split_input(input: list[str]) -> tuple[list[int], list[int]]:
    """Split the input into two lists"""

    list1: list[int] = []
    list2: list[int] = []

    # Idea for improvement: insert into a min heap and later pop from it,
    # that way it's already sorted and we can avoid the two sorts
    for line in input:
        [item1, item2] = line.split()
        list1.append(int(item1))
        list2.append(int(item2))

    return list1, list2


def part1(input: list[str]):
    print("Hello from part1!")

    list1, list2 = split_input(input)

    list1.sort()
    list2.sort()

    total_dst = 0
    for item1, item2 in zip(list1, list2):
        total_dst += abs(item1 - item2)

    return total_dst


def part2(input: list[str]):
    print("Hello from part2!")

    list1, list2 = split_input(input)

    counts: dict[int, int] = defaultdict(int)
    for item in list2:
        counts[item] += 1

    similarity = 0
    for item in list1:
        similarity += counts[item] * item

    return similarity
