from app.selector.selector import GenericSelector, Selector


class NamespaceSelector(GenericSelector):
    """
    Represents the namespace of the experiment's target Pod.

    Attributes
    ----------
    value : dict
        a formatted dict for yaml dumping
    """

    def __init__(self, *args):
        self.value = {Selector.namespaces.name: list(args)}
