from enum import IntEnum
from functools import lru_cache


class Status(IntEnum):
    OPENED = 1
    IN_PROGRESS = 2
    CLOSED = 3

    @classmethod
    @lru_cache(maxsize=1)
    def choices(cls) -> list[tuple[int, str]]:
        return [(status.value, status.name.lower().capitalize()) for status in cls]
