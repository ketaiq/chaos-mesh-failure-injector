from enum import Enum, unique, auto


@unique
class TaskType(Enum):
    """Represents task types of Chaos Mesh workflow."""

    Serial = auto()
    Parallel = auto()
