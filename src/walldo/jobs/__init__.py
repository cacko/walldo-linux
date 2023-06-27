from .rotate import rotate
from enum import StrEnum


class Job(StrEnum):
    ROTATE = "rotate"


class JobTrigger(StrEnum):
    INTERVAL = "interval"


__all__ = [
    "rotate",
]
