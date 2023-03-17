from enum import Enum, unique
import os
from app.selector.selector import Selector

PREFIX = "app.kubernetes.io"


@unique
class Label(Enum):
    """
    Represents valid shared labels of Kubernetes objects.

    See https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/
    """

    NAME = os.path.join(PREFIX, "name")
    INSTANCE = os.path.join(PREFIX, "instance")
    VERSION = os.path.join(PREFIX, "version")
    COMPONENT = os.path.join(PREFIX, "component")
    PART_OF = os.path.join(PREFIX, "part-of")
    MANAGED_BY = os.path.join(PREFIX, "managed-by")


class LabelSelector:
    """
    Represents the labels that the experiment's target Pod must have.

    Attributes
    ----------
    value : dict
        a formatted dict for yaml dumping
    """

    def __init__(self, labels: dict):
        self.value = {Selector.labelSelectors.name: {}}
        for key, value in labels.items():
            if key in [l.value for l in Label.__members__.values()]:
                self.value[Selector.labelSelectors.name][key] = value
