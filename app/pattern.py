from enum import Enum, unique, auto


@unique
class Pattern(Enum):
    CONSTANT = auto()
    LINEAR = auto()
    EXPONENTIAL = auto()
    RANDOM = auto()
