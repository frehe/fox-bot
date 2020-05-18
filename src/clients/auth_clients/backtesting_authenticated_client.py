from clients.auth_clients.my_authenticated_client import MyAuthenticatedClient

from backtesting.backtesting_engine import BacktestingEngine

from utilities.utils import UnixToISOTimestamp


class BacktestingAuthenticatedClient(MyAuthenticatedClient):
    def __init__(
            self, start_time: str, end_time: str, granularity: int,
            balances: dict, maker_fee: float, taker_fee: float,
            key="", b64secret="", passphrase="", api_url="backtest_auth"):
        super(BacktestingAuthenticatedClient, self).__init__(
            key, b64secret, passphrase, api_url)

        self.Engine = BacktestingEngine(
            start_time, end_time, granularity, balances, maker_fee, taker_fee)

    def get_time(self) -> dict:
        """[summary]

        Returns:
            dict -- Dict {
                'iso': 'YYYY-MM-DDThh:mm:ss.fffZ',
                'epoch': UNIX epoch
                }
        """
        current_epoch = BacktestingEngine.get_time()
        current_iso = UnixToISOTimestamp(current_epoch)

        return {
            'iso': current_iso,
            'epoch': current_epoch
        }

    def get_accounts(self) -> list:
        """Get a summary of all accounts with different currencies.

        Returns:
            list -- List of dicts containing keys
                            ['id', 'currency' 'balance', 'available']
        """
        return BacktestingEngine.get_accounts()

    def buy_taker(self, product: str, funds: str) -> dict:
        """Issue a buy order on the taker (market) side.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'
            funds {float} -- The amount of funds in base currency to use

        Returns:
            dict -- with keys ['id', 'product_id', 'side', 'funds',
                'specified_funds', 'executed_value', 'filled_size', 'type',
                'created_at', 'done_at', 'fill_fees', 'status', 'settled']
        """
        return BacktestingEngine.placeMarketOrder(
            product_id=product,
            side='buy',
            funds=funds
        )

    def buy_maker(self, product: str, price: str, size: str) -> dict:
        """Issue a buy order on the maker (limit) side.

        Arguments:
            product {str} -- [description]
            price {str} -- [description]
            size {str} -- [description]

        Returns:
            dict -- [description]
        """
        pass

    def sell_taker(self, product: str, size: str) -> dict:
        """Issue a sell order on the taker (market) side.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'
            funds {float} -- The amount of funds in base currency to use

        Returns:
            dict -- [description]
        """
        return BacktestingEngine.placeMarketOrder(
            product_id=product,
            side='sell',
            funds=size
        )

    def sell_maker(self, product: str, price: str, size: str) -> dict:
        """Issue a sell order on the maker (limit) side.

        Arguments:
            product {str} -- [description]
            price {str} -- [description]
            size {str} -- [description]

        Returns:
            dict -- [description]
        """
        pass

    def get_order(self, order_id: str) -> dict:
        """Get updated information on a placed order

        Arguments:
            order_id {str} -- The id by with to identify the order.

        Returns:
            dict -- Dictionary with keys ['id', 'product_id', 'side', 'funds',
                'specified_funds', 'executed_value', 'filled_size', 'type',
                'created_at', 'done_at', 'fill_fees', 'status', 'settled']
        """
        return BacktestingEngine.get_order(order_id)
