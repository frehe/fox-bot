from cbpro.public_client import PublicClient

from clients.public_clients.my_public_client import MyPublicClient


class CBProPublicClient(MyPublicClient):
    def __init__(self, api_url='https://api.pro.coinbase.com', timeout=30):
        super(CBProPublicClient, self).__init__(api_url, timeout)

        self.public_client = PublicClient(api_url, timeout)

    def get_time(self) -> dict:
        """Get current time from server.

        Returns:
            dict -- Dict {
                'iso': 'YYYY-MM-DDThh:mm:ss.fffZ',
                'epoch': UNIX epoch
                }
        """
        return self.public_client.get_time()

    def get_currencies(self) -> list:
        """List all known currencies.

        Returns:
            list -- List of dicts [
                {'id': 'BTC', 'name': 'Bitcoin', 'min_size': '0.00000001'},
                {'id': 'EUR', 'name': 'Euro', 'min_size': '0.01'},
                ...
                ]
        """
        return self.public_client.get_currencies()

    def get_product_24hr_stats(self, product: str) -> dict:
        """Get 24hr stats of a given product.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'

        Returns:
            dict -- Dict containing keys 'open', 'high', 'low', 'volume', 'last'
        """
        return self.public_client.get_product_24hr_stats(product)

    def get_product_historic_rates(
            self, product: str, start: str,
            end: str, granularity: int) -> list:
        """Obtain historic rate information between two timepoints.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'
            start {str} -- ISO 8601-formatted: 'YYYY-MM-DDThh:mm:ss.fffZ'
            end {str} -- ISO 8601-formatted: 'YYYY-MM-DDThh:mm:ss.fffZ'
            granularity {int} -- one of {60, 300, 900, 3600, 21600, 86400}

        Returns:
            list -- List of buckets. Each bucket contains data
                [time, low, high, open, close, volume] for the
                duration of granularity
        """
        return self.public_client.get_product_historic_rates(
            product_id=product,
            start=start,
            end=end,
            granularity=granularity
        )
