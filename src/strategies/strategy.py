import datetime

from abc import ABC

from backtesting.backtesting_engine import BacktestingEngine

from utilities.product_infos import ProductInfos
from utilities.data_handler import DataHandler
from utilities.utils import getWorkingDirectory, joinPaths


class Strategy(ABC):
    def __init__(
        self, buy_signal_generator, sell_signal_generator,
            risk_allocator, product: str, public_client,
            auth_client, config: dict):

        self.buy_signal_generator = buy_signal_generator
        self.sell_signal_generator = sell_signal_generator
        self.risk_allocator = risk_allocator
        self.product = product
        self.public_client = public_client
        self.auth_client = auth_client
        self.config = config

        self.data_handler = None

    def execute(self) -> bool:
        # create history folder to save all output to
        self._createHistory()
        self.data_handler.write_config(self.config)

        # Refresh information on the traded products
        ProductInfos.refresh(self.public_client, self.product)

        for _ in range(self.config['strategy_params']['episodes']):
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

    def backtest(self) -> bool:
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
            start_time=self.config['backtest']['start'],
            end_time=self.config['backtest']['end'],
            granularity=self.config['backtest']['granularity'],
            balances=self.config['backtest']['start_balances'],
            maker_fee=self.config['backtest']['maker_fee'],
            taker_fee=self.config['backtest']['taker_fee']
        )

        self.Backtest.activateProduct(self.product)

        return self.execute()

    def _createHistory(self):
        current_path = getWorkingDirectory()
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d--%H:%M:%S")
        dir_path = joinPaths([
            current_path, 'history', 'past_runs', timestamp])
        self.data_handler = DataHandler(dir_path)
