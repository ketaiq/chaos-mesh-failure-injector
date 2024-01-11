from app.chaos.network.action import (
    BandwidthAction,
    CorruptAction,
    DelayAction,
    DuplicateAction,
    LossAction,
)
from app.chaos.network.direction import Direction
from app.chaos.network.network_fault import NetworkFault
from app.chaos.stress.type import StressorType
import random, datetime
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


def gen_serial_cpu_stress(
    pattern: Pattern,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: dict,
    init_value: int,
    increment: int = 0,
    max_value: int = 0,
    suspend: int = 0,
):
    all_chaos = gen_serial_suspend(suspend)
    mode = Mode.ALL.value
    ls = LabelSelector(label)
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    selector = SelectorStruct(ns, ls, ps)
    value = init_value
    for _ in range(num_task):
        stressor = CPUStressor(value, 50)
        stress = Stress(
            f"{stressor.workers}workers-{stressor.load}load-cpu",
            f"{single_duration}m",
            mode,
            stressor,
            selector,
        )
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
        all_chaos.append(stress)

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    service = list(label.values())[0]
    workflow_name = f"{pattern.name.lower()}-cpu-stress-{service}-{time_suffix}"
    total_duration = single_duration * num_task + suspend
    if not suspend:
        workflow_name += "-without-suspend"
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_memory_stress(
    pattern: Pattern,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: dict,
    init_value: int,
    value_increment: int = 0,
    max_value: int = 0,
    suspend: int = 0,
    is_percentage: bool = False,
):
    all_chaos = gen_serial_suspend(suspend)
    mode = Mode.ALL.value
    ls = LabelSelector(label)
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    selector = SelectorStruct(ns, ls, ps)
    value = init_value
    for _ in range(num_task):
        if value > 50:
            time = "30s"
        else:
            time = None
        if is_percentage:
            stressor = MemoryStressor(f"{value}%", time=time, oomScoreAdj=-1000)
            stress = Stress(
                f"{value}percent-mem", f"{single_duration}m", mode, stressor, selector
            )
        else:
            stressor = MemoryStressor(f"{value}MB", time=time, oomScoreAdj=-1000)
            stress = Stress(
                f"{value}mb-mem", f"{single_duration}m", mode, stressor, selector
            )

        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += value_increment
        elif pattern is Pattern.EXPONENTIAL:
            # exponentially increase the value
            value *= value_increment
        elif pattern is Pattern.CONSTANT:
            # keep value as the initial value
            value = init_value
        elif pattern is Pattern.RANDOM:
            # randomly choose between the initial value and the maximum value
            value = random.randint(init_value, max_value)
        value = int(value)
        all_chaos.append(stress)

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    service = list(label.values())[0]
    workflow_name = f"{pattern.name.lower()}-memory-stress-{service}-{time_suffix}"
    total_duration = single_duration * num_task + suspend
    if not suspend:
        workflow_name += "-without-suspend"
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_network_duplicate(
    process_type: TaskType,
    pattern: Pattern,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: str,
    init_value: int,
    increment: int = 0,
    max_value: int = None,
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
        action = DuplicateAction(str(value), "0")
        network_fault = NetworkFault(
            f"{value}percent-duplicate",
            f"{single_duration}m",
            mode,
            selector,
            target_selector,
            action,
            Direction.TO,
        )
        all_chaos.append(network_fault)
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += increment
            if max_value is not None and value > max_value:
                value = max_value
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

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    workflow_name = f"{label}-{pattern.name.lower()}-network-duplicate-{time_suffix}"
    total_duration = single_duration * num_task + suspend
    w = Workflow(
        namespace,
        workflow_name,
        process_type,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_network_bandwidth(
    pattern: Pattern,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: str,
    init_value: int,
    decrement: int = 0,
    min_value: int = None,
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
        action = BandwidthAction(f"{value}kbps", 100, value * 100)
        network_fault = NetworkFault(
            f"{value}kbps-bandwidth",
            f"{single_duration}m",
            mode,
            selector,
            target_selector,
            action,
            Direction.TO,
        )
        all_chaos.append(network_fault)
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value -= decrement
            if min_value is not None and value < min_value:
                value = min_value
        elif pattern is Pattern.CONSTANT:
            # keep value as the initial value
            value = init_value
        value = int(value)

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    workflow_name = f"{pattern.name.lower()}-network-bandwidth-{label}-{time_suffix}"
    total_duration = single_duration * num_task + suspend
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_network_delay(
    pattern: Pattern,
    direction: Direction,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: dict,
    init_value: int,
    increment: int = 0,
    max_value: int = None,
    suspend: int = 0,
):
    all_chaos = gen_serial_suspend(suspend)
    mode = Mode.ALL.value
    ls = LabelSelector(label)
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
            direction,
        )
        all_chaos.append(network_fault)
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += increment
            if max_value is not None and value > max_value:
                value = max_value
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

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    service = list(label.values())[0]
    workflow_name = f"{pattern.name.lower()}-network-delay-{service}-{time_suffix}"
    total_duration = single_duration * num_task + suspend
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_network_loss(
    pattern: Pattern,
    direction: Direction,
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
        action = LossAction(str(value), "0")
        network_fault = NetworkFault(
            f"{value}-loss",
            f"{single_duration}m",
            mode,
            selector,
            target_selector,
            action,
            direction,
        )
        all_chaos.append(network_fault)
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += increment
            if value > 95:
                value = 95
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

    workflow_name = f"{pattern.name.lower()}-network-loss-{label}"
    total_duration = single_duration * num_task + suspend
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def _gen_serial_network_loss(
    pattern: Pattern, namespace: str, label: str, rates: list, periods: list
):
    """
    Generates a serial workflow to simulate network loss.

    Parameters
    ----------
    pattern : Pattern
        chosen pattern of change of stress
    namespace : str
    label : str
    rates : list
        list of integers indicating the intensity of injected failures
    periods : list
        list of integers indicating the number of minutes for each task, index 0 indicates time of suspending, index 1 indicates time of the first task
    """
    all_chaos = gen_serial_suspend(periods[0])
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: label})
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    selector = SelectorStruct(ns, ls, ps)
    target_selector = SelectorStruct(ns)

    if len(rates) + 1 != len(periods):
        print("rates and periods are not aligned!")
        return

    for i in range(len(rates)):
        value = rates[i]
        duration = periods[i + 1]
        action = LossAction(str(value), "0")
        network_fault = NetworkFault(
            f"{value}-loss",
            f"{duration}m",
            mode,
            selector,
            target_selector,
            action,
            Direction.TO,
        )
        all_chaos.append(network_fault)

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    workflow_name = f"{label}-{pattern.name.lower()}-network-loss-{time_suffix}"
    total_duration = sum(periods)
    w = Workflow(
        namespace,
        workflow_name,
        TaskType.Serial.name,
        convert_duration(total_duration),
        all_chaos,
    )
    w.dump_yaml()


def gen_serial_network_corrupt(
    pattern: Pattern,
    single_duration: int,
    num_task: int,
    namespace: str,
    label: str,
    init_value: int,
    increment: int = 0,
    max_value: int = None,
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
        action = CorruptAction(str(value), "0")
        network_fault = NetworkFault(
            f"{value}-corrupt",
            f"{single_duration}m",
            mode,
            selector,
            target_selector,
            action,
            Direction.TO,
        )
        all_chaos.append(network_fault)
        if pattern is Pattern.LINEAR:
            # linearly increase the value
            value += increment
            if max_value is not None and value > max_value:
                value = max_value
            if value > 100:
                value = 100
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

    time_suffix = datetime.datetime.now().strftime("%m%d%H")
    workflow_name = f"{pattern.name.lower()}-network-corrupt-{label}-{time_suffix}"
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
