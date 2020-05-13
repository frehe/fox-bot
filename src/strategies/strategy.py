import cbpro

from abc import ABC, abstractmethod
from utilities.product_infos import ProductInfos


class Strategy(ABC):
    def __init__(self, buy_signal_generator, sell_signal_generator, risk_allocator, product: str, public_client: cbpro.PublicClient, auth_client: cbpro.AuthenticatedClient):
        self.buy_signal_generator = buy_signal_generator
        self.sell_signal_generator = sell_signal_generator
        self.risk_allocator = risk_allocator
        self.product = product
        self.public_client = public_client
        self.auth_client = auth_client

    def execute(self) -> bool:
        # Refresh information on the traded products
        ProductInfos.refresh(self.public_client, self.product)

        # Launch buy signal generator and wait for signal
        buy_signal = self.buy_signal_generator.getSignal()

        # Allocate a risk value and create a trade from it
        buy_trade = self.risk_allocator.createBuyTrade(buy_signal)

        # Execute the trade
        trade_result = buy_trade.execute()
        print(trade_result)

        # Launch sell signal generator and wait for signal
        sell_signal = self.sell_signal_generator.getSignal(buy_signal)

        # Sell position
        sell_trade = self.risk_allocator.createSellTrade(sell_signal)

        # Execute the trade
        sell_trade = sell_trade.execute()
        print(sell_trade)

        return True



