from app.chaos.stress.stressor import MemoryStressor, CPUStressor


def test_init():
    m = MemoryStressor(2, 1, "1m", 3)
    c = CPUStressor(2, 1)
    assert m.value == {
        "memory": {
            "workers": 1,
            "size": 2,
            "time": "1m",
            "oomScoreAdj": 3,
        }
    }
    assert c.value == {"cpu": {"workers": 1, "load": 2}}


def main():
    test_init()


if __name__ == "__main__":
    main()
