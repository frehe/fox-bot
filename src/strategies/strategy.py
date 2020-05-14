import cbpro
import datetime

from abc import ABC

from utilities.product_infos import ProductInfos
from utilities.data_handler import DataHandler


class Strategy(ABC):
    def __init__(
        self, buy_signal_generator, sell_signal_generator,
            risk_allocator, product: str, public_client: cbpro.PublicClient,
            auth_client: cbpro.AuthenticatedClient):

        self.buy_signal_generator = buy_signal_generator
        self.sell_signal_generator = sell_signal_generator
        self.risk_allocator = risk_allocator
        self.product = product
        self.public_client = public_client
        self.auth_client = auth_client
        self.strategy_active = True

        self.data_handler = None

    def execute(self) -> bool:
        # create history folder to save all output to
        self._createHistory()

        # Refresh information on the traded products
        ProductInfos.refresh(self.public_client, self.product)

        while self.strategy_active is True:
            # Launch buy signal generator and wait for signal
            buy_signal = self.buy_signal_generator.getSignal()

            # Allocate a risk value and create a trade from it
            buy_trade = self.risk_allocator.createBuyTrade(buy_signal)

            # Execute the trade
            trade_result = buy_trade.execute()

            # Log trade
            self.data_handler.write_trade_history(trade_result)
            self.data_handler.write_balances(self.auth_client, self.product)

            # Launch sell signal generator and wait for signal
            sell_signal = self.sell_signal_generator.getSignal(buy_signal)

            # Sell position
            sell_trade = self.risk_allocator.createSellTrade(sell_signal)

            # Execute the trade
            trade_result = sell_trade.execute()
            
            self.data_handler.write_trade_history(trade_result)
            self.data_handler.write_balances(self.auth_client, self.product)

        return True

    def _createHistory(self):
        dir_path = "./trading_bot/history/past_runs/"
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d--%H:%M:%S")
        dir_path += (timestamp + "/")
        self.data_handler = DataHandler(dir_path)
