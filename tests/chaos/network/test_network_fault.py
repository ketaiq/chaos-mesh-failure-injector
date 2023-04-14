import yaml
from yaml import Loader
from app.chaos.mode import Mode
from app.chaos.network.action import DelayAction
from app.chaos.network.direction import Direction
from app.chaos.network.network_fault import NetworkFault
from app.selector.label import Label, LabelSelector
from app.selector.namespace import NamespaceSelector
from app.selector.pod_phase import PodPhase, PodPhaseSelector
from app.selector.selector import SelectorStruct


def test_init():
    name = "10mb-mem"
    duration = "10m"
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: "identity"})
    ns = NamespaceSelector("alms")
    ps = PodPhaseSelector(PodPhase.Running.name)
    s = SelectorStruct(ls, ns, ps)
    action = DelayAction("10s", "50", "1s")
    direction = Direction.BOTH
    network_fault = NetworkFault(name, duration, mode, s, action, direction)
    print(yaml.dump(network_fault.value))

if __name__ == "__main__":
    test_init()
