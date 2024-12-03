from ..main import is_safe


def test_is_safe_increasing_input():
    input = [1, 2, 3, 4, 5]
    assert is_safe(input) is True


def test_is_safe_increasing_input_in_diff_range():
    input = [1, 2, 7, 10, 11]
    assert is_safe(input) is False


def test_is_safe_decreasing_input():
    input = [5, 4, 3, 2, 1]
    assert is_safe(input) is True


def test_is_safe_decreasing_input_outside_diff_range():
    input = [20, 19, 15, 10, 5]
    assert is_safe(input) is False


def test_is_safe_mixed_input_in_diff_range():
    input = [1, 3, 4, 2, 5]
    assert is_safe(input) is False


def test_is_safe_mixed_input_outside_diff_range():
    input = [8, 4, 5, 1, 3]
    assert is_safe(input) is False


def test_is_safe_repeating_numbers():
    input = [5, 6, 6, 7, 8]
    assert is_safe(input) is False
