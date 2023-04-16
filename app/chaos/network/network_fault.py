from app.chaos.chaos import Chaos
from app.chaos.kind import Kind
from app.chaos.network.action import Action
from app.chaos.network.direction import Direction
from app.selector.selector import SelectorStruct


class NetworkFault(Chaos):
    def __init__(
        self,
        name: str,
        duration: str,
        mode: str,
        selector: SelectorStruct,
        target_selector: SelectorStruct,
        action: Action,
        direction: Direction,
    ):
        super().__init__(name, Kind.NetworkChaos.name, duration)
        action_type = action.TYPE
        self.value["networkChaos"] = {
            "selector": selector.value,
            "mode": mode,
            "action": action_type,
            action_type: action.get_value(),
            "direction": direction.name.lower(),
            "target": {"selector": target_selector.value, "mode": mode},
        }
