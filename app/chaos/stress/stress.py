from app.chaos.chaos import Chaos
from app.chaos.stress.stressor import Stressor
from typing import Type
from app.chaos.kind import Kind
from app.selector.selector import SelectorStruct


class Stress(Chaos):
    def __init__(
        self,
        name: str,
        duration: str,
        mode: str,
        stressors: Type[Stressor],
        selector: SelectorStruct,
    ):
        super().__init__(name, Kind.StressChaos.name, duration)
        self.value["stressChaos"] = {
            "selector": selector.value,
            "mode": mode,
            "stressors": stressors.value,
        }
