from app.chaos.stress.stressor import MemoryStressor
from app.chaos.stress.stress import Stress
from app.selector.selector import SelectorStruct
from app.selector.pod_phase import PodPhaseSelector, PodPhase
from app.selector.label import LabelSelector, Label
from app.selector.namespace import NamespaceSelector
from app.workflow.workflow import Workflow
from app.chaos.kind import Kind
from app.chaos.mode import Mode
from app.workflow.task_type import TaskType
import yaml


def test_init():
    name1 = "10mb-mem"
    name2 = "20mb-mem"
    duration = "10m"
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: "identity"})
    ns = NamespaceSelector("alms")
    ps = PodPhaseSelector(PodPhase.Running.name)
    s = SelectorStruct(ls, ns, ps)
    m = MemoryStressor(1, 2, "1m", 3)
    stress1 = Stress(name1, duration, mode, m, s)
    stress2 = Stress(name2, duration, mode, m, s)
    w = Workflow(
        "alms", "linear-memory-stress", TaskType.Serial.name, "20m", [stress1, stress2]
    )
    yaml.Dumper.ignore_aliases = lambda *args: True
    yaml_dump = yaml.dump(w.value)
    assert yaml_dump == yaml.dump(
        {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "Workflow",
            "metadata": {"namespace": "alms", "name": "linear-memory-stress"},
            "spec": {
                "entry": "entry",
                "templates": [
                    {
                        "name": "entry",
                        "templateType": "Serial",
                        "deadline": "20m",
                        "children": [name1, name2],
                    },
                    {
                        "name": name1,
                        "templateType": Kind.StressChaos.name,
                        "deadline": duration,
                        "stressChaos": {
                            "mode": mode,
                            "selector": {
                                "labelSelectors": {
                                    "app.kubernetes.io/name": "identity"
                                },
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
                    },
                    {
                        "name": name2,
                        "templateType": Kind.StressChaos.name,
                        "deadline": duration,
                        "stressChaos": {
                            "mode": mode,
                            "selector": {
                                "labelSelectors": {
                                    "app.kubernetes.io/name": "identity"
                                },
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
                    },
                ],
            },
        }
    )


def main():
    test_init()


if __name__ == "__main__":
    main()
