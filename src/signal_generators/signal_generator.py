from abc import ABC, abstractmethod 

from clients.public_clients.my_public_client import MyPublicClient


class SignalGenerator(ABC):
    def __init__(
            self, public_client: MyPublicClient, product: str,
            timespan: int = 0):
        self.public_client = public_client
        self.product = product
        self.timespan = timespan
        self.signal = False

    def getSignal(self):
        pass

    def _printStatus(self):
        pass
