from app.chaos.chaos import Chaos
from app import API_VERSION
from typing import Type
import yaml


class Entry:
    """Defines the entry of the workflow when the workflow is being executed."""

    def __init__(self, templateType, deadline, children: list[str]):
        self.value = {
            "name": "entry",
            "templateType": templateType,
            "deadline": deadline,
            "children": children,
        }


class Workflow:
    """
    Represents a built-in workflow engine. Using this engine,
    you can run different Chaos experiments in serial or parallel
    to simulate production-level errors.
    """

    def __init__(
        self,
        namespace: str,
        name: str,
        templateType: str,
        deadline: str,
        all_chaos: list[Type[Chaos]],
    ):
        entry = Entry(
            templateType, deadline, [chaos.value["name"] for chaos in all_chaos]
        )
        templates = [entry.value]
        templates.extend([chaos.value for chaos in all_chaos])
        self.value = {
            "apiVersion": API_VERSION,
            "kind": "Workflow",
            "metadata": {"namespace": namespace, "name": name},
            "spec": {"entry": "entry", "templates": templates},
        }
        self.name = name

    def dump_yaml(
        self,
    ):
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(f"{self.name}.yaml", "w") as f:
            yaml.dump(self.value, f, sort_keys=False)
