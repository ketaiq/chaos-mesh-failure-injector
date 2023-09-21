from enum import Enum, unique, auto
from dataclasses import dataclass
from typing import ClassVar


@unique
class ActionType(Enum):
    DELAY = auto()
    LOSS = auto()
    DUPLICATE = auto()
    CORRUPT = auto()
    PARTITION = auto()
    BANDWIDTH = auto()


class Action:
    def get_value(self) -> dict:
        """Return a dict containing non-empty attributes."""
        value = {}
        for attr in self.__dict__.keys():
            if self.__dict__[attr]:
                value[attr] = self.__dict__[attr]
        return value


@dataclass
class DelayAction(Action):
    TYPE: ClassVar[str] = ActionType.DELAY.name.lower()
    latency: str
    correlation: str
    jitter: str


@dataclass
class LossAction(Action):
    TYPE: ClassVar[str] = ActionType.LOSS.name.lower()
    loss: str
    correlation: str


@dataclass
class CorruptAction(Action):
    TYPE: ClassVar[str] = ActionType.CORRUPT.name.lower()
    corrupt: str
    correlation: str


@dataclass
class DuplicateAction(Action):
    TYPE: ClassVar[str] = ActionType.DUPLICATE.name.lower()
    duplicate: str
    correlation: str


@dataclass
class BandwidthAction(Action):
    TYPE: ClassVar[str] = ActionType.BANDWIDTH.name.lower()
    rate: str
    limit: str
    buffer: str
