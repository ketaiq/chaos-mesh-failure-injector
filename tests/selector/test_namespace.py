from app.selector.namespace import NamespaceSelector
import yaml

def test_init():
    ns = NamespaceSelector("alms")
    yaml_dump = yaml.dump(ns.value)
    assert yaml_dump == yaml.dump({"namespaces": ["alms"]})

def main():
    test_init()


if __name__ == "__main__":
    main()