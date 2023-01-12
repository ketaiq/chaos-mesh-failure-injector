from app.failures.failure import Failure


class NetworkFailure(Failure):
    def __init__(self, address: str, name: str, duration: str):
        self.address = address
        self.name = name
        self.duration = duration
