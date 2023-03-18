from app.chaos.chaos import Chaos
from app.chaos.kind import Kind


class Suspend(Chaos):
    def __init__(self, duration: str):
        super().__init__("suspending", Kind.Suspend.name, duration)
