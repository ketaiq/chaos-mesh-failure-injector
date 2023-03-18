class Stressor:
    def __init__(self, value: dict):
        self.value = value


class MemoryStressor(Stressor):
    """Specifies the memory stress."""

    def __init__(
        self, workers: int, size: str, time: str = None, oomScoreAdj: int = None
    ):
        value = {
            "memory": {
                "workers": workers,
                "size": size,
            }
        }
        if time:
            value["memory"]["time"] = time
        if oomScoreAdj:
            value["memory"]["oomScoreAdj"] = oomScoreAdj
        super().__init__(value)


class CPUStressor(Stressor):
    """Specifies the CPU stress."""

    def __init__(self, workers: int, load: int):
        super().__init__({"cpu": {"workers": workers, "load": load}})
