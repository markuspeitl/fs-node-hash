import os
from typing import Callable


def snap_times(path: str) -> list[float]:
    original_stat = os.stat(path)
    original_atime = original_stat.st_atime
    original_mtime = original_stat.st_mtime

    return [original_atime, original_mtime]


def restore_times(path: str, times: list[float]):
    os.utime(path, (times[0], times[1]))


def time_transient(to_wrap_fn: Callable) -> Callable:
    def wrapper_fn(path: str, *args):
        current_times = snap_times(path)
        res = to_wrap_fn(path, *args)
        restore_times(path, current_times)
        return res

    return wrapper_fn
