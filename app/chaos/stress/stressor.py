class Stressor:
    def __init__(self, value: dict):
        self.value = value


class MemoryStressor(Stressor):
    """Specifies the memory stress."""

    def __init__(self, workers: int, size: str, time: str, oomScoreAdj: int):
        super().__init__(
            {
                "memory": {
                    "workers": workers,
                    "size": size,
                    "time": time,
                    "oomScoreAdj": oomScoreAdj,
                }
            }
        )


class CPUStressor(Stressor):
    """Specifies the CPU stress."""

    def __init__(self, workers: int, load: int):
        super().__init__({"cpu": {"workers": workers, "load": load}})
