import cbpro

from trades.trade import Trade


class RiskAllocator():
    def __init__(self, authClient: cbpro.AuthenticatedClient, product: str):
        self.product = product
        self.available_buy = None
        self.available_sell = None
    
    def createTrade() -> Trade:
        pass
