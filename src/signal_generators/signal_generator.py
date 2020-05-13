import cbpro

from abc import ABC, abstractmethod 


class SignalGenerator(ABC):
    def __init__(self, public_client: cbpro.PublicClient, product: str, timespan: int=0):
        self.public_client = public_client
        self.product = product
        self.timespan = timespan
        self.signal = False

    def getSignal(self):
        pass