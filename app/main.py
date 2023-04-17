from app.experiment import (
    gen_linear_memory_stress,
    gen_linear_cpu_stress,
    gen_linear_cpu_stress_without_suspend,
    gen_serial_network_delay,
)
from app.pattern import Pattern
from app.utils.string import print_failure_period
from datetime import timedelta


def main():
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
    gen_serial_network_delay(
        Pattern.LINEAR, 18, 10, "alms", "userapi", 50, 50, suspend=10
    )


if __name__ == "__main__":
    main()
