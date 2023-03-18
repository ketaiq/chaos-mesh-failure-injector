from app.chaos.chaos import Chaos
from app.chaos.kind import Kind


class Suspend(Chaos):
    def __init__(self, name: str, duration: str):
        super().__init__(name, Kind.Suspend.name, duration)
