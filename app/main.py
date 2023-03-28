from app.experiment import (
    gen_linear_memory_stress,
    gen_linear_cpu_stress,
    gen_linear_cpu_stress_without_suspend,
)
from app.utils.string import print_failure_period
from datetime import timedelta


def main():
    # gen_linear_memory_stress("identity")
    # gen_linear_memory_stress("userhandlers")
    # gen_linear_cpu_stress("identity")
    # gen_linear_cpu_stress("userhandlers")
    print_failure_period(
        "27/03/2023, 14:26:28", timedelta(hours=9, minutes=10), timedelta(hours=3)
    )


if __name__ == "__main__":
    main()
