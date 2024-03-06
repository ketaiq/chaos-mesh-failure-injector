from app.chaos.network.direction import Direction
from app.chaos.stress.config import CPUStressorConfig
from app.experiment import (
    _gen_serial_network_loss,
    gen_linear_memory_stress,
    gen_linear_cpu_stress,
    gen_linear_cpu_stress_without_suspend,
    gen_network_duplicate,
    gen_serial_cpu_stress,
    gen_serial_memory_stress,
    gen_serial_network_bandwidth,
    gen_serial_network_corrupt,
    gen_serial_network_delay,
    gen_serial_network_loss,
)
from app.pattern import Pattern
from app.selector.label import Label
from app.utils.string import print_failure_period
from datetime import timedelta

from app.workflow.task_type import TaskType


def inject_failure_in_train_ticket():
    # CPU stress
    # gen_serial_cpu_stress(
    #     Pattern.LINEAR,
    #     5,
    #     24,
    #     "default",
    #     {Label.APP.value: "ts-train-service"},
    #     10,
    #     10,
    #     suspend=120,
    # )
    gen_serial_memory_stress(
        Pattern.LINEAR,
        2,
        60,
        "default",
        {Label.APP.value: "ts-station-service"},
        500,
        30,
        suspend=120,
    )
    gen_serial_network_delay(
        Pattern.LINEAR,
        Direction.BOTH,
        5,
        24,
        "default",
        {Label.APP.value: "ts-train-service"},
        1000,
        1000,
        suspend=120,
        max_value=30000,
    )


def main():
    inject_failure_in_train_ticket()
    # gen_linear_memory_stress("identity")
    # gen_linear_memory_stress("userhandlers")
    # gen_linear_cpu_stress("identity")
    # gen_linear_cpu_stress("userhandlers")
    # print_failure_period(
    #     "27/03/2023, 14:26:28", timedelta(hours=9, minutes=10), timedelta(hours=3)
    # )

    # gen_serial_network_delay(
    #     Pattern.LINEAR, 5, 36, "alms", "userhandlers", 50, 50, suspend=550
    # )
    # gen_serial_network_delay(
    #     Pattern.LINEAR, 10, 18, "alms", "scorm", 50, 50, suspend=10
    # )
    # gen_serial_network_delay(
    #     Pattern.LINEAR, 20, 9, "alms", "userapi", 500, 500, suspend=60
    # )

    # gen_serial_network_loss(Pattern.LINEAR, 9, 20, "alms", "userapi", 5, 5, suspend=60)

    # gen_serial_network_corrupt(
    #     Pattern.LINEAR, 9, 20, "alms", "userapi", 5, 5, suspend=60
    # )

    # gen_serial_network_corrupt(
    #     Pattern.CONSTANT, 5, 24, "alms", "userapi", 85, suspend=30
    # )

    # gen_serial_network_loss(Pattern.CONSTANT, 5, 24, "alms", "userapi", 50, suspend=30)

    # gen_serial_network_delay(Pattern.CONSTANT, 5, 24, "alms", "userapi", 2500, suspend=30)

    # gen_serial_cpu_stress(Pattern.CONSTANT, 5, 24, "alms", {Label.NAME.value: "userapi"}, 500, suspend=30)

    # gen_serial_cpu_stress(
    #     Pattern.LINEAR, 5, 24, "default", {Label.APP.value: "ts-auth-service"}, 10, 5, suspend=30
    # )

    # gen_serial_cpu_stress(
    #     Pattern.LINEAR,
    #     5,
    #     24,
    #     "alms",
    #     {Label.NAME.value: "rui"},
    #     10,
    #     5,
    #     suspend=30,
    # )

    # gen_serial_memory_stress(
    #     Pattern.CONSTANT, 5, 24, "alms", "userapi", 320, suspend=30
    # )

    # gen_serial_memory_stress(
    #     Pattern.LINEAR, 5, 24, "alms", "userapi", 290, 2, suspend=30
    # )

    # gen_serial_memory_stress(
    #     Pattern.LINEAR, 1, 120, "default", {Label.APP.value: "ts-auth-service"}, 5, 5, suspend=30
    # )

    # gen_serial_memory_stress(
    #     Pattern.LINEAR,
    #     2,
    #     60,
    #     "default",
    #     {Label.APP.value: "ts-auth-service"},
    #     100,
    #     16,
    #     suspend=30,
    # )

    # gen_serial_memory_stress(
    #     Pattern.LINEAR,
    #     1,
    #     120,
    #     "alms",
    #     {Label.NAME.value: "mail-sender-web"},
    #     5,
    #     5,
    #     suspend=30,
    # )

    # gen_serial_network_corrupt(
    #     Pattern.LINEAR, 5, 24, "alms", "redis", 20, 5, suspend=30, max_value=70
    # )

    # gen_serial_network_loss(Pattern.LINEAR, 5, 24, "alms", "userapi", 20, 5, suspend=30)
    # gen_serial_network_loss(Pattern.LINEAR, 10, 12, "alms", "userapi", 10, 10, suspend=30)

    # gen_serial_network_delay(
    #     Pattern.LINEAR,
    #     Direction.BOTH,
    #     10,
    #     12,
    #     "alms",
    #     {Label.NAME.value: "userhandlers"},
    #     1000,
    #     1000,
    #     suspend=30,
    #     max_value=10000,
    # )

    # gen_serial_network_delay(
    #     Pattern.LINEAR,
    #     Direction.BOTH,
    #     10,
    #     12,
    #     "alms",
    #     {Label.NAME.value: "identity"},
    #     1000,
    #     1000,
    #     suspend=30,
    #     max_value=10000,
    # )

    # gen_serial_network_delay(
    #     Pattern.LINEAR,
    #     Direction.BOTH,
    #     10,
    #     12,
    #     "alms",
    #     {Label.NAME.value: "scorm"},
    #     1000,
    #     1000,
    #     suspend=30,
    #     max_value=10000,
    # )

    # train ticket
    # gen_serial_network_delay(
    #     Pattern.LINEAR,
    #     Direction.BOTH,
    #     10,
    #     12,
    #     "default",
    #     {Label.APP.value: "ts-auth-service"},
    #     1000,
    #     500,
    #     suspend=30,
    #     max_value=5000,
    # )

    # _gen_serial_network_loss(
    #     Pattern.LINEAR, "alms", "userapi", [50, 60, 70, 80], [120, 30, 30, 30, 30]
    # )

    # gen_network_duplicate(
    #     TaskType.Serial.name,
    #     Pattern.LINEAR,
    #     10,
    #     12,
    #     "alms",
    #     "userapi",
    #     50,
    #     50,
    #     suspend=30,
    #     max_value=100,
    # )

    # gen_serial_network_bandwidth(
    #     Pattern.LINEAR, 10, 12, "alms", "userapi", 5000, 500, min_value=1, suspend=30
    # )

    # gen_serial_network_corrupt(
    #     Pattern.LINEAR, 10, 18, "alms", "redis", 20, 5, suspend=30, max_value=90
    # )

    # gen_serial_network_loss(
    #     Pattern.LINEAR,
    #     Direction.BOTH,
    #     10,
    #     18,
    #     "alms",
    #     "redis",
    #     20,
    #     5,
    #     suspend=30,
    # )

    # gen_serial_network_delay(
    #     Pattern.LINEAR,
    #     Direction.BOTH,
    #     10,
    #     12,
    #     "alms",
    #     "identity",
    #     1000,
    #     500,
    #     suspend=30,
    # )


if __name__ == "__main__":
    main()
