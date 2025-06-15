from enum import StrEnum, auto
from functools import lru_cache


class Role(StrEnum):
    ADMIN = auto()
    SENIOR = auto()
    JUNIOR = auto()

    @classmethod
    @lru_cache(maxsize=1)
    def users(cls):
        return [cls.SENIOR, cls.JUNIOR]

    @classmethod
    @lru_cache(maxsize=1)
    def choices(cls) -> list[tuple[str, str]]:
        return [(role.value, role.name.lower().capitalize()) for role in cls]
