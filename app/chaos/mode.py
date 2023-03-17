from enum import Enum, unique


@unique
class Mode(Enum):
    """Represents the mode of Chaos Mesh experiments."""

    ONE = "one"
    ALL = "all"
    FIXED = "fixed"
    FIXED_PERCENT = "fixed-percent"
    RANDOM_MAX_PERCENT = "random-max-percent"
