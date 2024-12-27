from time import perf_counter
from typing import Callable, ParamSpec, TypeVar


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
        print(f"Calculated in {value:.2f} {unit}")

        return result

    return wrapper
