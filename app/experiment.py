from app.chaos.stress.type import StressorType
import random
from app.chaos.mode import Mode
from app.chaos.stress.config import (
    MemoryStressorConfig,
    CPUStressorConfig,
    StressorConfig,
)
from app.chaos.stress.stress import Stress
from app.chaos.stress.stressor import MemoryStressor, CPUStressor
from app.selector.label import Label, LabelSelector
from app.selector.namespace import NamespaceSelector
from app.selector.pod_phase import PodPhase, PodPhaseSelector
from app.selector.selector import SelectorStruct
from app.workflow.task_type import TaskType
from app.workflow.workflow import Workflow
from app.chaos.suspend import Suspend
from app.pattern import Pattern
from app.utils.string import convert_duration


def gen_linear_memory_stress(label: str):
    config = MemoryStressorConfig(5, 5)
    gen_serial_stress(config, Pattern.LINEAR, 5, 730, "alms", label, 550)


def gen_linear_cpu_stress(label: str):
    config = CPUStressorConfig(2, 2)
    gen_serial_stress(config, Pattern.LINEAR, 3, 730, "alms", label, 550)


def gen_serial_stress(
    config: StressorConfig,
    pattern: Pattern,
    single_duration: int,
    duration: int,
    namespace: str,
    label: str,
    suspend: int = None,
):
    """
    Generates a serial workflow to simulate stress.

    Parameters
    ----------
    config : StressorConfig
        configuration of chosen stressor
    pattern : Pattern
        chosen pattern of change of stress
    single_duration : int
        duration of each Chaos experiment in minutes
    duration : int
        duration of the workflow in minutes
    namespace : str
        chosen namespace where the Chaos experiment takes effect
    label : str
        chosen label that the experiment's target Pod must have
    suspend : int
        suspending time in minutes before the Chaos experiment
    """
    all_chaos = []
    if suspend:
        remain_suspend = suspend
        suspend_index = 1
        while remain_suspend > 0:
            if remain_suspend >= 60:
                all_chaos.append(Suspend(f"suspending{suspend_index}", "1h"))
                remain_suspend -= 60
            else:
                all_chaos.append(
                    Suspend(f"suspending{suspend_index}", f"{remain_suspend}m")
                )
                break
            suspend_index += 1
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: label})
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    selector = SelectorStruct(ns, ls, ps)
    value = config.init_value
    for _ in range((duration - suspend) // single_duration):
        if config.type is StressorType.MEMORY:
            stressor = MemoryStressor(f"{value}MB", oomScoreAdj=-1000)
            stress = Stress(
                f"{value}mb-mem", f"{single_duration}m", mode, stressor, selector
            )
        elif config.type is StressorType.CPU:
            stressor = CPUStressor(value)
            stress = Stress(
                f"{value}percent-cpu", f"{single_duration}m", mode, stressor, selector
            )
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += config.increment
        elif pattern is Pattern.EXPONENTIAL:
            # exponentially increase the value
            value *= config.increment
        elif pattern is Pattern.CONSTANT:
            # keep value as the initial value
            value = config.init_value
        elif pattern is Pattern.RANDOM:
            # randomly choose between the initial value and the maximum value
            value = random.randint(config.init_value, config.max_value)
        value = int(value)
        all_chaos.append(stress)

    w = Workflow(
        namespace,
        f"{pattern.name.lower()}-{config.type.name.lower()}-stress",
        TaskType.Serial.name,
        convert_duration(duration),
        all_chaos,
    )
    w.dump_yaml()
