import csv

from pycoingecko import CoinGeckoAPI
from utilities.utils import \
    getIDOfCurrencyCoinGecko, UnixToISOTimestamp, ISOToUnixTimestamp, \
    getIndexOfCurrency, getIndexOfOrder, getIndexOfClosestEpoch
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
                granularity {int} -- Collect backtesting data with
                                        this granularity in seconds
                balances {dict} -- Init wallets with these balances
                                        e.g. {'BTC': '100.000', ...}
            """
            self.time_grid = []
            # TODO: Write a data loader that provides a desired granularity
            assert granularity in [3600, 86400], \
                "Only hour-wise or day-wise granularity is supported so far."
            self.granularity = granularity

            self.cg = CoinGeckoAPI()

            # Convert start and end dates to epoch
            self.start_epoch = int(ISOToUnixTimestamp(start_time))
            self.end_epoch = int(ISOToUnixTimestamp(end_time))
            self.current_relative_epochs = {}

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

            self._setBalances(balances)

            # Orders
            self.orders = []

            # Load market data from start_epoch to end_epoch
            self.price_data = {}

            # Set active product
            self.active_product = ""

        def _setBalances(self, balances: dict):
            for key, value in balances.items():
                idx = getIndexOfCurrency(self.accounts, key)
                self.accounts[idx]['available'] = str(value)

    instance = None

    def __init__(
            self, start_time: str, end_time: str, granularity: int,
            balances: dict, maker_fee: float, taker_fee: float):
        if not BacktestingEngine.instance:
            BacktestingEngine.instance = BacktestingEngine.__BacktestingEngine(
                start_time, end_time, granularity,
                balances, maker_fee, taker_fee)
        else:
            raise ValueError("Backtesting Singleton instance already exists.")

    # def __getattribute__(self, n):
    #     return getattr(self.instance, n)

    @staticmethod
    def clearPriceData(product: str):
        BacktestingEngine.instance.price_data.pop(product, None)
        BacktestingEngine.instance.current_relative_epochs.pop(product, None)

    @staticmethod
    def activateProduct(product: str):
        if product not in BacktestingEngine.instance.price_data:
            BacktestingEngine._loadPriceData(product)
        BacktestingEngine.instance.active_product = product

    @staticmethod
    def get_time() -> int:
        return BacktestingEngine.instance.price_data[
            BacktestingEngine.instance.active_product][
                BacktestingEngine.instance.current_relative_epochs[
                    BacktestingEngine.instance.active_product]][
                0]

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
        buy_account = BacktestingEngine.instance.accounts[getIndexOfCurrency(
            BacktestingEngine.instance.accounts, buy_currency)]
        base_account = BacktestingEngine.instance.accounts[getIndexOfCurrency(
            BacktestingEngine.instance.accounts, base_currency)]

        if side == 'buy':
            # Check if balance is sufficient
            available_base = float(base_account['available'])

            if available_base < funds:
                return [{'ErrorMessage': 'Funds are insufficient'}]

            # Remove funds from balance
            base_account['available'] = str(available_base - funds)

            # Calculate how much is bought and remove fees
            buy_amount = \
                (1.0 * funds) / BacktestingEngine._get_rate(
                    product_id,
                    BacktestingEngine.instance.current_relative_epochs[
                        BacktestingEngine.instance.active_product]
                    )
            fill_fees = \
                BacktestingEngine.instance.maker_fee * buy_amount
            filled_size = \
                buy_amount - fill_fees
            buy_account['available'] = \
                str(float(buy_account['available']) + filled_size)

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
            available_buy = float(buy_account['available'])

            if float(available_buy) < funds:
                return [{'ErrorMessage': 'Funds are insufficient'}]

            # Remove funds from balance
            buy_account['available'] = str(available_buy - funds)

            # Calculate how much is bought and remove fees
            base_amount = \
                1.0 * funds * BacktestingEngine._get_rate(
                    product_id,
                    BacktestingEngine.instance.current_relative_epochs[
                        BacktestingEngine.instance.active_product]
                    )
            fill_fees = \
                BacktestingEngine.instance.maker_fee * base_amount
            filled_size = \
                base_amount - fill_fees
            base_account['available'] = \
                str(float(base_account['available']) + filled_size)

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
        return BacktestingEngine.instance.orders[
            getIndexOfOrder(BacktestingEngine.instance.orders, order_id)]

    @staticmethod
    def get_currencies():
        return CurrenciesDetail.detail.value

    @staticmethod
    def get_product_24hr_stats(product: str):
        """Obtain 24hr stats of a given product

        Arguments:
            product {str} -- [description]
        """
        # Get closest relative epoch of 24 hrs ago
        current_epoch = \
            BacktestingEngine.instance.current_relative_epochs[product]
        past_epoch = \
            BacktestingEngine._absolute_to_relative_epoch(
                product,
                BacktestingEngine._relative_to_absolute_epoch(
                    product, current_epoch) - 24 * 60 * 60)  # go back 24 hrs
        open_rate = BacktestingEngine._get_rate(product, past_epoch)
        close_rate = BacktestingEngine._get_rate(product, current_epoch)
        max_rate = max([
            entry[5] for entry in
            BacktestingEngine.instance.price_data[product][
                past_epoch:current_epoch + 1]
            ])
        min_rate = min([
            entry[5] for entry in
            BacktestingEngine.instance.price_data[product][
                past_epoch:current_epoch + 1]]
            )

        return {
            'open': str(open_rate),
            'last': str(close_rate),
            'high': str(max_rate),
            'low': str(min_rate),
            'volume': "NaN"
        }

    @staticmethod
    def get_product_historic_rates(
            product: str, start: str, end: str, granularity: int) -> list:
        """Obtain a list of historic rate buckets.

        Arguments:
            product {str} -- [description]
            start {str} -- ISO time
            end {str} -- ISO time
            granularity {int} -- [description]

        Returns:
            list -- List of buckets. Each bucket contains data
                [time, low, high, open, close, volume] for the
                duration of granularity
        """
        assert granularity == BacktestingEngine.instance.granularity, \
            "Granularity of backtesting engine and desired rates do not match"

        # Convert ISO times to Unix epochs
        start_epoch = int(ISOToUnixTimestamp(start))
        end_epoch = int(ISOToUnixTimestamp(end))

        start_epoch_relative = BacktestingEngine._absolute_to_relative_epoch(product, start_epoch)
        end_epoch_relative = BacktestingEngine._absolute_to_relative_epoch(product, end_epoch)

        result = []

        for i, entry in enumerate(BacktestingEngine.instance.price_data[
                product][start_epoch_relative:end_epoch_relative + 1]):
            open_rate = entry[4]
            close_rate = \
                BacktestingEngine.instance.price_data[product][i + 1][7]
            result.append([
                BacktestingEngine._relative_to_absolute_epoch(product, i),
                max(open_rate, close_rate),
                min(open_rate, close_rate),
                open_rate,
                close_rate,
                None
            ])
        
        return result

    @staticmethod
    def _loadPriceData(product: str):
        print('Loading price data for backtest on pair: ' + product)
        # buy_currency = product[:3]
        # base_currency = product[-3:]
        # coins_list = BacktestingEngine.instance.cg.get_coins_list()
        # buy_currency_id = \
        #     getIDOfCurrencyCoinGecko(coins_list, buy_currency)

        # TODO: Load with BaktestingEngine.instance.granularity
        # prices = \
        #     BacktestingEngine.instance.cg \
        #     .get_coin_market_chart_range_by_id(
        #         id=buy_currency_id,
        #         vs_currency=base_currency.lower(),
        #         from_timestamp=BacktestingEngine.instance.start_epoch,
        #         to_timestamp=BacktestingEngine.instance.end_epoch
        #     )['prices']

        # for i, elem in enumerate(prices):
        #     elem[0] = int(elem[0] / 1000.)

        path_granularity = ''
        if BacktestingEngine.instance.granularity == 3600:
            path_granularity = '_1h'
        elif BacktestingEngine.instance.granularity == 86400:
            path_granularity = '_1d'

        filepath = (
            "./trading_bot/resources/historic_data/"
            + product + '/'
            + product + path_granularity
            + '.csv')

        with open(filepath, newline='') as f:
            reader = csv.reader(f, delimiter=";")
            prices = list(reader)[1:]
            for elem in prices:
                elem[0] = int(elem[0])
                for i in range(4, len(elem)):
                    elem[i] = float(elem[i])
            prices.reverse()

        # Data has headers UNIX Timestamp, Excel Timestamp, Date, Symbol,
        # Open, High, Low, Close, Volume buy_currency, Volume base_currency

        BacktestingEngine.instance.price_data[product] = prices

        BacktestingEngine.instance.current_relative_epochs[product] = \
            getIndexOfClosestEpoch(
                prices, BacktestingEngine.instance.start_epoch)

    @staticmethod
    def advance_time() -> bool:
        """Simulate the progression of time.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'

        Returns:
            bool -- True if end epoch reached, otherwise False.
        """
        product = BacktestingEngine.instance.active_product
        BacktestingEngine.instance.current_relative_epochs[product] += 1

        if (BacktestingEngine.instance.current_relative_epochs[product]
                >= len(BacktestingEngine.instance.price_data[product])):
            raise ValueError('No historic data available for specified timepoint.')
        if (
            BacktestingEngine._relative_to_absolute_epoch(
                product,
                BacktestingEngine.instance.current_relative_epochs[product])
                >= BacktestingEngine.instance.end_epoch):
            raise Exception('End of backtesting period reached.')
        return False

    @staticmethod
    def _get_rate(product: str, rel_epoch: int) -> float:
        """Return the exchange rate at the current timepoint in simulation.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'

        Returns:
            float -- exchange rate: price in base currency
        """
        return BacktestingEngine.instance.price_data[product][
            rel_epoch
        ][7]

    @staticmethod
    def _relative_to_absolute_epoch(product: str, rel_epoch: int) -> int:
        """[summary]

        Arguments:
            product {str} -- [description]
            rel_epoch {int} -- Relative index in price_data

        Returns:
            int -- UNIX-formatted epoch corresponding to the absolute time
        """
        return BacktestingEngine.instance.price_data[product][rel_epoch][0]

    @staticmethod
    def _absolute_to_relative_epoch(product: str, abs_epoch: int):
        """[summary]

        Arguments:
            product {str} -- [description]
            abs_epoch {int} -- A timepoint in the past, UNIX-formatted

        Returns:
            [type] -- the array index of the closest timepoint in price_data
        """
        return getIndexOfClosestEpoch(
            BacktestingEngine.instance.price_data[product],
            abs_epoch)
