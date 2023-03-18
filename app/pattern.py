from app.chaos.mode import Mode
from app.chaos.stress.stress import Stress
from app.chaos.stress.stressor import MemoryStressor, CPUStressor
from app.selector.label import Label, LabelSelector
from app.selector.namespace import NamespaceSelector
from app.selector.pod_phase import PodPhase, PodPhaseSelector
from app.selector.selector import SelectorStruct
from app.workflow.task_type import TaskType
from app.workflow.workflow import Workflow


def gen_linear_memory_stress(
    init_size: int,
    single_duration: int,
    size_increment: int,
    duration: int,
    namespace: str,
    label: str,
):
    """
    Generates a serial workflow to simulate memory stress in a linear pattern.

    Parameters
    ----------
    init_size : int
        initial memory size in megabytes to be occupied
    single_duration : int
        duration of each Chaos experiment in minutes
    size_increment : int
        increment of memory size in megabytes
    duration : int
        duration of the workflow in minutes
    namespace : str
        chosen namespace where the Chaos experiment takes effect
    label : str
        chosen label that the experiment's target Pod must have
    """

    all_chaos = []
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: label})
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    s = SelectorStruct(ns, ls, ps)
    size = init_size
    for _ in range(duration // single_duration):
        m = MemoryStressor(3, f"{size}MB", oomScoreAdj=-1000)
        stress = Stress(f"{size}mb-mem", f"{single_duration}m", mode, m, s)
        size += size_increment
        all_chaos.append(stress)
    w = Workflow(
        namespace,
        "linear-memory-stress",
        TaskType.Serial.name,
        f"{duration}m",
        all_chaos,
    )
    w.dump_yaml()


def gen_linear_cpu_stress(
    init_load: int,
    single_duration: int,
    load_increment: int,
    duration: int,
    namespace: str,
    label: str,
):
    """
    Generates a serial workflow to simulate CPU stress in a linear pattern.

    Parameters
    ----------
    init_load : int
        initial percentage of CPU to be occupied
    single_duration : int
        duration of each Chaos experiment in minutes
    load_increment : int
        increment of percentage of CPU
    duration : int
        duration of the workflow in minutes
    namespace : str
        chosen namespace where the Chaos experiment takes effect
    label : str
        chosen label that the experiment's target Pod must have
    """
    all_chaos = []
    mode = Mode.ALL.value
    ls = LabelSelector({Label.NAME.value: label})
    ns = NamespaceSelector(namespace)
    ps = PodPhaseSelector(PodPhase.Running.name)
    s = SelectorStruct(ns, ls, ps)
    load = init_load
    for _ in range(duration // single_duration):
        c = CPUStressor(1, load)
        stress = Stress(f"{load}percent-cpu", f"{single_duration}m", mode, c, s)
        load += load_increment
        all_chaos.append(stress)
    w = Workflow(
        namespace,
        "linear-cpu-stress",
        TaskType.Serial.name,
        f"{duration}m",
        all_chaos,
    )
    w.dump_yaml()
