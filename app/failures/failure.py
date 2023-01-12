from abc import ABC, abstractmethod


class Failure(ABC):
    @abstractmethod
    def _create(self):
        pass

    @abstractmethod
    def _recover(self):
        pass
