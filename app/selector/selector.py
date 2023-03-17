from enum import Enum, unique, auto
from abc import ABC


class GenericSelector(ABC):
    pass


@unique
class Selector(Enum):
    """
    Represents valid selector types of Chaos Mesh experiments.

    See https://chaos-mesh.org/docs/define-chaos-experiment-scope/
    """

    namespaces = auto()
    labelSelectors = auto()
    expressionSelectors = auto()
    annotationSelectors = auto()
    fieldSelectors = auto()
    podPhaseSelectors = auto()
    nodeSelectors = auto()
    nodes = auto()
    pods = auto()
    physicalMachines = auto()


class SelectorStruct:
    """
    Specifies the target Pod.

    Attributes
    ----------
    value : dict
        a formatted dict for yaml dumping"""

    def __init__(self, *args):
        self.value = {}
        for arg in args:
            if issubclass(type(arg), GenericSelector):
                for key, value in arg.value.items():
                    if key in [l for l, _ in Selector.__members__.items()]:
                        self.value[key] = value
