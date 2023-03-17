from app.selector.label import LabelSelector
from app.selector.valid_label import ValidLabel
import yaml


def test_init():
    label_selector = LabelSelector({ValidLabel.NAME.value: "identity"})
    yaml_dump = yaml.dump(label_selector.value)
    assert yaml_dump == yaml.dump(
        {"labelSelectors": {"app.kubernetes.io/name": "identity"}}
    )


def main():
    test_init()


if __name__ == "__main__":
    main()
