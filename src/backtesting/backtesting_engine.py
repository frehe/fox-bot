from pycoingecko import CoinGeckoAPI

from strategies.strategy import Strategy
from utilities.utils import \
    getIDOfCurrencyCoinGecko, UnixToISOTimestamp, ISOToUnixTimestamp, \
    getIndexOfCurrency, getIndexOfOrder
from utilities.enums import Currencies, CurrenciesDetail


class BacktestingEngine():
    class __BacktestingEngine():
        def __init__(
                self, start_time: str, end_time: str, granularity: int,
                balances: dict, maker_fee: float, taker_fee: float):
            """The backtesting engine models the backend of an exchange.

            Data produced by this engine is accessed through its own client.

            Arguments:
                start_time {int} -- ISO 8601
                end_time {int} -- ISO 8601
                granularity {int} -- Collect backtesting data with this granularity.
                balances {dict} -- Init wallets with these balances
                                    e.g. {'BTC': '100.000', ...}
            """

            self.time_grid = []
            self.granularity = granularity  # TODO: Write a data loader that provides a desired granularity.

            self.price_data = None
            self.cg = CoinGeckoAPI()

            # Convert start and end dates to epoch
            self.start_epoch = int(ISOToUnixTimestamp(start_time))
            self.end_epoch = int(ISOToUnixTimestamp(end_time))
            self.current_epoch = self.start_epoch

            # Fees
            self.maker_fee = maker_fee
            self.taker_fee = taker_fee

            # Accounts and available products
            self.currencies = [c.value for c in Currencies]
            self.accounts = \
                [{
                    "id": "account_" + str(self.currencies.index(currency)),
                    "currency": currency,
                    "balance": "0.0",
                    "available": "0.0",
                    "hold": "0.0",
                    "profile_id": "backtest",
                } for currency in self.currencies]

            # Orders
            self.orders = []

    instance = None

    def __init__(
            self, start_time: str, end_time: str, granularity: int,
            balances: dict, maker_fee: float, taker_fee: float):
        if not BacktestingEngine.instance:
            BacktestingEngine.instance = BacktestingEngine.instance(
                start_time, end_time, granularity,
                balances, maker_fee, taker_fee
            )
        else:
            raise ValueError("Backtesting Singleton instance already exists.")

    def __getattribute__(self, n):
        return getattr(self.instance, n)

    @staticmethod
    def get_time() -> int:
        return BacktestingEngine.instance.current_epoch

    @staticmethod
    def get_accounts() -> list:
        return BacktestingEngine.instance.accounts

    @staticmethod
    def placeMarketOrder(
            product_id: str, side: str, funds: str) -> dict:
        """Place a simulated market order.

        Arguments:
            product_id {str} -- e.g. 'BTC-EUR'
            side {str} -- 'buy' or 'sell'
            funds {str} -- 'buy': amount in EUR to use, 'sell': amount in BTC to sell.

        Returns:
            dict -- [description]
        """

        funds = float(funds)
        buy_currency = product_id[:3]
        base_currency = product_id[-3:]
        buy_account = BacktestingEngine.instance.accounts[getIndexOfCurrency(buy_currency)]
        base_account = BacktestingEngine.instance.accounts[getIndexOfCurrency(base_currency)]

        if side == 'buy':
            # Check if balance is sufficient
            available_base = base_account['available']

            if available_base < funds:
                return [{'ErrorMessage': 'Funds are insufficient'}]

            # Remove funds from balance
            base_account['available'] -= funds

            # Calculate how much is bought and remove fees
            buy_amount = (1.0 * funds) / BacktestingEngine._get_current_rate(product_id)
            fill_fees = BacktestingEngine.instance.maker_fee * buy_amount
            filled_size = buy_amount - fill_fees
            buy_account['available'] += filled_size

            output = {
                'id': 'backtest_order_' + str(BacktestingEngine.get_time()),
                'product_id': product_id,
                'side': side,
                'funds': str(funds),
                'specified_funds': str(funds),
                'executed_value': str(funds),
                'filled_size': str(filled_size),
                'type': 'market',
                'created_at': UnixToISOTimestamp(BacktestingEngine.get_time()),
                'done_at': UnixToISOTimestamp(BacktestingEngine.get_time()),
                'fill_fees': str(fill_fees),
                'status': 'done',
                'settled': True
            }

        elif side == 'sell':
            # Check if balance is sufficient
            available_buy = buy_account['available']

            if available_buy < funds:
                return [{'ErrorMessage': 'Funds are insufficient'}]

            # Remove funds from balance
            buy_account['available'] -= funds

            # Calculate how much is bought and remove fees
            base_amount = 1.0 * funds * BacktestingEngine._get_current_rate(product_id)
            fill_fees = BacktestingEngine.instance.maker_fee * base_amount
            filled_size = base_amount - fill_fees
            base_account['available'] += filled_size

            output = {
                'id': 'backtest_order_' + str(BacktestingEngine.get_time()),
                'product_id': product_id,
                'side': side,
                'funds': "",
                'specified_funds': "",
                'executed_value': str(base_amount),
                'filled_size': str(funds),
                'type': 'market',
                'created_at': UnixToISOTimestamp(BacktestingEngine.get_time()),
                'done_at': UnixToISOTimestamp(BacktestingEngine.get_time()),
                'fill_fees': str(fill_fees),
                'status': 'done',
                'settled': True
            }
        else:
            return ValueError('Order Type must be buy or sell.')

        BacktestingEngine.instance.orders.append(output)
        return output

    @staticmethod
    def get_order(order_id: str):
        return BacktestingEngine.instance.orders[getIndexOfOrder(order_id)]

    @staticmethod
    def get_currencies():
        return CurrenciesDetail.detail
    
    @staticmethod
    def get_product_24hr_stats(product: str):
        """Obtain 24hr stats of a given product

        Arguments:
            product {str} -- [description]
        """
        pass

    @staticmethod
    def get_product_historic_rates(
            product_id: str, start: str, end: str, granularity: int):
        """Obtain a list of historic rate buckets.

        Arguments:
            product_id {str} -- [description]
            start {str} -- [description]
            end {str} -- [description]
            granularity {int} -- [description]
        """
        pass

    # @staticmethod
    # def loadPriceData():
    #     coins_list = BacktestingEngine.cg.get_coins_list()
    #     buy_currency_id = \
    #         getIDOfCurrencyCoinGecko(coins_list, self.buy_currency)

    #     self.price_data = self.cg.get_coin_market_chart_range_by_id(
    #         id=buy_currency_id,
    #         vs_currency=self.base_currency.lower(),
    #         from_timestamp=self.start_epoch,
    #         to_timestamp=self.end_epoch)['prices']

    @staticmethod
    def createAnalysis(strategy: Strategy):
        """Analyze the performance of a provided strategy.

        Arguments:
            strategy {Strategy} -- The strategy to analyze
        """
        pass

    @staticmethod
    def _advance_time() -> bool:
        """Simulate the progression of time.

        Returns:
            bool -- True if end epoch reached, otherwise False.
        """
        BacktestingEngine.instance.current_epoch \
            += BacktestingEngine.instance.granularity

        if (BacktestingEngine.instance.current_epoch
                >= BacktestingEngine.instance.end_epoch):
            return True
        return False

    @staticmethod
    def _get_current_rate(produt: str) -> float:
        """Return the exchange rate at the current timepoint in simulation.

        Arguments:
            produt {str} -- e.g. 'BTC-EUR'

        Returns:
            float -- exchange rate: price in base currency
        """
        pass
