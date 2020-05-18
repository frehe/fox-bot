from cbpro.authenticated_client import AuthenticatedClient

from clients.auth_clients.my_authenticated_client import MyAuthenticatedClient


class CBProAuthenticatedClient(MyAuthenticatedClient):
    def __init__(
            self, key: str, b64secret: str, passphrase: str,
            api_url="https://api.pro.coinbase.com"):

        super(CBProAuthenticatedClient, self).__init__(
            key, b64secret, passphrase, api_url)

        self.auth_client = AuthenticatedClient(
            key=key,
            b64secret=b64secret,
            passphrase=passphrase,
            api_url=api_url
        )

    def get_time(self) -> dict:
        """[summary]

        Returns:
            dict -- Dict {
                'iso': 'YYYY-MM-DDThh:mm:ss.fffZ',
                'epoch': UNIX epoch
                }
        """
        return self.auth_client.get_time()

    def get_accounts(self) -> list:
        """Get a summary of all accounts with different currencies.

        Returns:
            list -- List of dicts containing keys
                            ['id', 'currency' 'balance', 'available']
        """
        return self.auth_client.get_accounts()

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
        return self.auth_client.place_market_order(
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
        return self.auth_client.place_market_order(
            product_id=product,
            side='sell',
            size=size
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
            id {str} -- The id by with to identify the order.

        Returns:
            dict -- Dictionary with keys ['id', 'product_id', 'side', 'funds',
                'specified_funds', 'executed_value', 'filled_size', 'type',
                'created_at', 'done_at', 'fill_fees', 'status', 'settled']
        """
        return self.auth_client.get_order(order_id)
