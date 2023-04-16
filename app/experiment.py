from app.chaos.network.action import DelayAction
from app.chaos.network.direction import Direction
from app.chaos.network.network_fault import NetworkFault
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
from dataclasses import dataclass


def gen_linear_memory_stress(label: str):
    config = MemoryStressorConfig(5, 5)
    gen_serial_stress(config, Pattern.LINEAR, 5, 730, "alms", label, 550)


def gen_linear_cpu_stress(label: str):
    config = CPUStressorConfig(5, 5)
    gen_serial_stress(config, Pattern.LINEAR, 5, 730, "alms", label, 550)


def gen_linear_cpu_stress_without_suspend(label: str):
    config = CPUStressorConfig(10, 10)
    gen_serial_stress(config, Pattern.LINEAR, 5, 730, "alms", label, 550)


def gen_serial_stress(
    config: StressorConfig,
    pattern: Pattern,
    single_duration: int,
    duration: int,
    namespace: str,
    label: str,
    suspend: int = 0,
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
    all_chaos = gen_serial_suspend(suspend)
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
            if value >= 100:
                config.increment = 100
            stressor = CPUStressor.calculate_config(value)
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

    workflow_name = f"{label}-{pattern.name.lower()}-{config.type.name.lower()}-stress"
    if not suspend:
        workflow_name += "-without-suspend"
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_network_delay(
    pattern: Pattern,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: str,
    init_value: int,
    increment: int = 0,
    max_value: int = 0,
    suspend: int = 0,
):
    all_chaos = gen_serial_suspend(suspend)
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: label})
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    selector = SelectorStruct(ns, ls, ps)
    target_selector = SelectorStruct(ns)
    value = init_value

    for _ in range(num_task):
        action = DelayAction(f"{value}ms", "0", "0ms")
        network_fault = NetworkFault(
            f"{value}ms-delay",
            f"{single_duration}m",
            mode,
            selector,
            target_selector,
            action,
            Direction.BOTH,
        )
        all_chaos.append(network_fault)
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += increment
        elif pattern is Pattern.EXPONENTIAL:
            # exponentially increase the value
            value *= increment
        elif pattern is Pattern.CONSTANT:
            # keep value as the initial value
            value = init_value
        elif pattern is Pattern.RANDOM:
            # randomly choose between the initial value and the maximum value
            value = random.randint(init_value, max_value)
        value = int(value)

    workflow_name = f"{label}-{pattern.name.lower()}-network-delay"
    total_duration = single_duration * num_task + suspend
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_suspend(suspend: int) -> list:
    tasks = []
    if suspend:
        remain_suspend = suspend
        i = 1
        while remain_suspend > 0:
            if remain_suspend >= 60:
                tasks.append(Suspend(f"suspending{i}", "1h"))
                remain_suspend -= 60
            else:
                tasks.append(Suspend(f"suspending{i}", f"{remain_suspend}m"))
                break
            i += 1
    return tasks
