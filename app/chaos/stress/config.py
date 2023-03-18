from app.chaos.stress.type import StressorType


class StressorConfig:
    def __init__(
        self, init_value: int, increment: float, max_value: int, type: StressorType
    ):
        self.init_value = init_value
        self.increment = increment
        self.max_value = max_value
        self.type = type


class MemoryStressorConfig(StressorConfig):
    """
    Represents a configuration of the memory stressor.

    Attributes
    ----------
    init_value : int
        initial memory size in megabytes to be occupied
    increment : float
        increment of memory size in megabytes
    max_value : int
        maximum memory size in megabytes to be occupied, only works with random pattern
    """

    def __init__(self, init_size: int, size_increment: float, max_value: int = None):
        super().__init__(init_size, size_increment, max_value, StressorType.MEMORY)


class CPUStressorConfig(StressorConfig):
    """
    Represents a configuration of the CPU stressor.

    Attributes
    ----------
    init_value : int
        initial percentage of CPU to be occupied
    increment : float
        increment of percentage of CPU
    max_value : int
        maximum percentage of CPU to be occupied, 100 by default, only works with random pattern
    """

    def __init__(self, init_load: int, load_increment: float, max_value: int = 100):
        max_value = 100 if max_value > 100 else max_value
        super().__init__(init_load, load_increment, max_value, StressorType.CPU)
