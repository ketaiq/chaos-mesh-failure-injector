from enum import Enum, unique, auto


@unique
class Kind(Enum):
    """Represents types of Chaos Mesh experiments."""

    Suspend = auto()
    StressChaos = auto()
    NetworkChaos = auto()
