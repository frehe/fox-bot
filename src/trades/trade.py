import cbpro

from abc import ABC, abstractmethod

class Trade(ABC):
    def __init__(self, authClient: cbpro.AuthenticatedClient):
        self.authClient = authClient
        super().__init__()

    @abstractmethod
    def execute(self):
        pass
