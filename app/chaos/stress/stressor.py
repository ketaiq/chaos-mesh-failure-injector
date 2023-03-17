from abc import ABC


class Stressor(ABC):
    pass


class MemoryStressor(Stressor):
    def __init__(self, workers: int, size: str, time: str, oomScoreAdj: int):
        self.value = {}


class CPUStressor(Stressor):
    def __init__(self, workers: int, load: int):
        self.value = {}
