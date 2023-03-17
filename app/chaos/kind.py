from enum import Enum, unique, auto


@unique
class Kind(Enum):
    """Represents types of Chaos Mesh experiments."""

    StressChaos = auto()
    NetworkChaos = auto()
