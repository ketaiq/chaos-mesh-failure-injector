from app.selector.selector import SelectorStruct
from app.selector.pod_phase import PodPhaseSelector, PodPhase
from app.selector.label import LabelSelector, Label
from app.selector.namespace import NamespaceSelector
import yaml


def test_init():
    ls = LabelSelector({Label.NAME.value: "identity"})
    ns = NamespaceSelector("alms")
    ps = PodPhaseSelector(PodPhase.Running.name)
    s = SelectorStruct(ls, ns, ps)
    yaml_dump = yaml.dump(s.value)
    assert yaml_dump == yaml.dump(
        {
            "labelSelectors": {"app.kubernetes.io/name": "identity"},
            "namespaces": ["alms"],
            "podPhaseSelectors": ["Running"],
        }
    )


def main():
    test_init()


if __name__ == "__main__":
    main()
