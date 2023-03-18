from enum import Enum, unique, auto

@unique
class StressorType(Enum):
    MEMORY = auto()
    CPU = auto()