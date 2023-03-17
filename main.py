from app.chaos.stress.stressor import MemoryStressor
from app.chaos.stress.stress import Stress
from app.selector.selector import SelectorStruct
from app.selector.pod_phase import PodPhaseSelector, PodPhase
from app.selector.label import LabelSelector, Label
from app.selector.namespace import NamespaceSelector
from app.workflow.workflow import Workflow
from app.chaos.mode import Mode
from app.workflow.task_type import TaskType


def main():
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
    w.dump_yaml()


if __name__ == "__main__":
    main()
