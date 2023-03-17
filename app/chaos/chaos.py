from abc import ABC, abstractmethod


class Chaos(ABC):
    @abstractmethod
    def create_experiment(self):
        pass
