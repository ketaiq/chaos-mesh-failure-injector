from app.chaos.stress.stressor import MemoryStressor
from app.chaos.stress.stress import Stress
from app.selector.selector import SelectorStruct
from app.selector.pod_phase import PodPhaseSelector, PodPhase
from app.selector.label import LabelSelector, Label
from app.selector.namespace import NamespaceSelector
from app.chaos.kind import Kind
from app.chaos.mode import Mode
import yaml


def test_init():
    name = "10mb-mem"
    duration = "10m"
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: "identity"})
    ns = NamespaceSelector("alms")
    ps = PodPhaseSelector(PodPhase.Running.name)
    s = SelectorStruct(ls, ns, ps)
    m = MemoryStressor(1, 2, "1m", 3)
    result = Stress(name, duration, mode, m, s)
    yaml_dump = yaml.dump(result.value)
    assert yaml_dump == yaml.dump(
        {
            "name": name,
            "templateType": Kind.StressChaos.name,
            "deadline": duration,
            "stressChaos": {
                "mode": mode,
                "selector": {
                    "labelSelectors": {"app.kubernetes.io/name": "identity"},
                    "namespaces": ["alms"],
                    "podPhaseSelectors": ["Running"],
                },
                "stressors": {
                    "memory": {
                        "workers": 1,
                        "size": 2,
                        "time": "1m",
                        "oomScoreAdj": 3,
                    },
                },
            },
        }
    )


def main():
    test_init()


if __name__ == "__main__":
    main()
