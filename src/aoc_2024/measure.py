from time import perf_counter
import tracemalloc
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


def format_memory(bytes: int) -> tuple[float, str]:
    if bytes < 1024**2:  # Less than 1 KiB
        return bytes, "bytes"
    elif bytes < 1024**3:  # Less than 1 MiB
        return bytes / 1024, "KiB"
    elif bytes < 1024**4:  # Less than 1 GiB
        return bytes / 1024**3, "MiB"
    else:
        return bytes / 1024**4, "GiB"


P = ParamSpec("P")
R = TypeVar("R")


def measure(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        tracemalloc.start()
        start = perf_counter()

        result = func(*args, **kwargs)

        end = perf_counter()

        memory = format_memory(tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()

        time_taken = end - start
        value, unit = format_time(time_taken)
        print(f"Calculated in {value:.2f} {unit}")
        print(f"Peak memory used: {memory[0] / 1024:.2f} {memory[1]}")

        return result

    return wrapper
