from app.experiment import gen_linear_memory_stress, gen_linear_cpu_stress


def main():
    # gen_linear_memory_stress("identity")
    gen_linear_memory_stress("userhandlers")
    # gen_linear_cpu_stress("identity")
    gen_linear_cpu_stress("userhandlers")


if __name__ == "__main__":
    main()
