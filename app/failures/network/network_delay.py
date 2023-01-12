from app.failures.network.network import NetworkFailure
import requests
import pandas as pd
from datetime import datetime
import time


class NetworkDelayFailure(NetworkFailure):
    def __init__(self, address: str, name: str, duration: str, **kwargs):
        self.latency = None
        self.jitter = None
        self.correlation = None
        self.device = None
        self.hostname = None
        self.ip = None
        self.protocol = None
        self.source_port = None
        self.egress_port = None
        self.uid = None
        super().__init__(address, name, duration)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def submit(self):
        start_time = datetime.now()
        end_time = start_time + pd.Timedelta(self.duration)
        self._create()
        # add 10 seconds padding
        while datetime.now() < end_time + pd.Timedelta("10s"):
            time.sleep(1)
        self._recover()

    def _create(self):
        """Creates a network failure."""
        payload = self._get_config()
        r = requests.post(
            "http://" + self.address + "/api/attack/network", json=payload
        )
        r.raise_for_status()
        self.uid = r.json()["uid"]

    def _recover(self):
        """Recovers a network failure."""
        r = requests.delete("http://" + self.address + "/api/attack/" + self.uid)
        r.raise_for_status()

    def _get_config(self) -> dict:
        config = {"action": "delay", "device": self.device, "latency": self.latency}
        if self.jitter is not None:
            config["jitter"] = self.jitter
        if self.correlation is not None:
            config["correlation"] = self.correlation
        if self.hostname is not None:
            config["hostname"] = self.hostname
        if self.ip is not None:
            config["ip-address"] = self.ip
        if self.protocol is not None:
            config["ip-protocol"] = self.protocol
        if self.source_port is not None:
            config["source-port"] = self.source_port
        if self.egress_port is not None:
            config["egress-port"] = self.egress_port
        return config
