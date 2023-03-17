from app.selector.pod_phase import PodPhaseSelector, PodPhase
import yaml


def test_init():
    ps = PodPhaseSelector(PodPhase.Running.name)
    yaml_dump = yaml.dump(ps.value)
    assert yaml_dump == yaml.dump({"podPhaseSelectors": ["Running"]})


def main():
    test_init()


if __name__ == "__main__":
    main()
