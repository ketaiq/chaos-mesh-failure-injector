from enum import Enum, unique, auto
from app.selector.selector import Selector


@unique
class PodPhase(Enum):
    """
    Represents valid phases of Kubernetes Pods.

    See https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
    """

    Pending = auto()
    Running = auto()
    Succeeded = auto()
    Failed = auto()
    Unknown = auto()
class PodPhaseSelector:
    """
    Represents the phase of the experiment's target Pod.

    Attributes
    ----------
    value : dict
        a formatted dict for yaml dumping
    """

    def __init__(self, *args):
        self.value = {Selector.podPhaseSelectors.name: list(args)}