from abc import ABC


class MyAuthenticatedClient(ABC):
    def __init__(self, key, b64secret, passphrase, api_url):
        super(MyAuthenticatedClient, self).__init__()
        self.key = key
        self.b64secret = b64secret
        self.passphrase = passphrase
        self.api_url = api_url

        self.auth_client = None

    def get_time(self) -> dict:
        """Get current time from server.

        Returns:
            dict -- Dict {
                'iso': 'YYYY-MM-DDThh:mm:ss.fffZ',
                'epoch': UNIX epoch
                }
        """
        pass

    def get_accounts(self) -> list:
        """Get a summary of all accounts with different currencies.

        Returns:
            list -- List of dicts containing keys
                            ['id', 'currency' 'balance', 'available']
        """
        pass

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
        pass

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

    def sell_taker(self, product: str, funds: str) -> dict:
        """Issue a sell order on the taker (market) side.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'
            funds {float} -- The amount of funds in base currency to use

        Returns:
            dict -- [description]
        """
        pass

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
        pass
