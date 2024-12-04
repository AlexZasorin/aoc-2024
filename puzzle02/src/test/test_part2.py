import pytest

from ..main import is_mostly_increasing, is_safe_recursive


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], True),
        ([8, 6, 4, 4, 1], True),
        ([1, 3, 6, 7, 9], True),
        ([1, 3, 3, 3, 4], False),
        ([100, 1, 2, 3, 4], True),
        ([100, 4, 3, 2, 1], True),
        ([1, 100, 101, 102, 103], True),
        ([100, 101, 2, 103, 104], True),
    ],
)
def test_part_2(test_input: list[int], expected: bool):
    assert (
        is_safe_recursive(test_input, is_mostly_increasing(test_input), 0, 1, 1)
        is expected
    )
