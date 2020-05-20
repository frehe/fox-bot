import datetime

from abc import ABC

# from clients.auth_clients.my_authenticated_client import MyAuthenticatedClient
# from clients.public_clients.my_public_client import MyPublicClient
from clients.auth_clients.backtesting_authenticated_client \
    import BacktestingAuthenticatedClient
from clients.public_clients.backtesting_public_client \
    import BacktestingPublicClient

from backtesting.backtesting_engine import BacktestingEngine

from utilities.product_infos import ProductInfos
from utilities.data_handler import DataHandler


class Strategy(ABC):
    def __init__(
        self, buy_signal_generator, sell_signal_generator,
            risk_allocator, product: str, public_client,
            auth_client):

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

    def backtest(
            self, start_time: str, end_time: str, granularity: int,
            balances: dict, maker_fee: float, taker_fee: float) -> bool:
        """Run a backtest on strategy.

        Arguments:
            start_time {str} -- ISO-formatted
            end_time {str} -- ISO-formatted
            granularity {int} -- Seconds between timepoints
            balances {dict} -- Init wallets with these balances
                                    e.g. {'BTC': '100.000', ...}
            maker_fee {float} -- Transaction fee for limit orders
            taker_fee {float} -- Transaction fee for market orders

        Returns:
            bool -- Returns True when strategy successfully completes
        """
        # Init backtesting engine
        self.Backtest = BacktestingEngine(
            start_time=start_time,
            end_time=end_time,
            granularity=granularity,
            balances=balances,
            maker_fee=maker_fee,
            taker_fee=taker_fee
        )

        self.Backtest.activateProduct(self.product)

        self.auth_client = BacktestingAuthenticatedClient()
        self.public_client = BacktestingPublicClient()
        return self.execute()

    def _createHistory(self):
        dir_path = "./trading_bot/history/past_runs/"
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d--%H:%M:%S")
        dir_path += (timestamp + "/")
        self.data_handler = DataHandler(dir_path)
