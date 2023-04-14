from enum import Enum, unique, auto


@unique
class Direction(Enum):
    FROM = auto()
    TO = auto()
    BOTH = auto()
