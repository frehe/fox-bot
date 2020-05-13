import cbpro

from abc import ABC

from signals.buy_signal import BuySignal
from signals.sell_signal import SellSignal
from signals.signal import Signal

from trades.buy_trade import BuyTrade
from trades.sell_trade import SellTrade


class RiskAllocator(ABC):
    def __init__(self, auth_client: cbpro.AuthenticatedClient, product: str):
        self.auth_client = auth_client
        self.product = product
        self.available_buy = None
        self.available_sell = None
    
    def createBuyTrade(self, buy_signal: BuySignal) -> BuyTrade:
        pass

    def createSellTrade(self, sell_signal: SellSignal) -> SellTrade:
        pass
