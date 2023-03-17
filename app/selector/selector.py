from enum import Enum, unique, auto


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
