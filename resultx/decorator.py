from typing import Callable

from resultx.result import Result


def result(func: Callable):
    def inner(*args, **kwargs):
        try:
            return Result.from_val(func(*args, **kwargs))
        except Exception as e:
            return Result.from_err(e)
    return inner
