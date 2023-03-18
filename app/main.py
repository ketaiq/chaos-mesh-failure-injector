from app.experiment import gen_serial_stress
from app.chaos.stress.config import MemoryStressorConfig
from app.pattern import Pattern

def main():
    config = MemoryStressorConfig(5, 5)
    gen_serial_stress(config, Pattern.LINEAR, 5, 730, "alms", "identity", 550)


if __name__ == "__main__":
    main()
