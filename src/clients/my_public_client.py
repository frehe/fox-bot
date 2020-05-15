from abc import ABC


class MyPublicClient(ABC):
    def __init__(self, api_url, timeout):
        super(MyPublicClient, self).__init__()

        self.api_url = api_url
        self.timeout = timeout

        self.public_client = None

    def get_time(self) -> dict:
        """Get current time from server.

        Returns:
            dict -- Dict {
                'iso': 'YYYY-MM-DDThh:mm:ss.fffZ',
                'epoch': UNIX epoch
                }
        """
        pass

    def get_currencies(self) -> list:
        """List all known currencies.

        Returns:
            list -- List of dicts [
                {'id': 'BTC', 'name': 'Bitcoin', 'min_size': '0.00000001'},
                {'id': 'EUR', 'name': 'Euro', 'min_size': '0.01'},
                ...
                ]
        """
        pass

    def get_product_24hr_stats(self, product: str) -> dict:
        """Get 24hr stats of a given product.

        Arguments:
            product {str} -- e.g. 'BTC-EUR'

        Returns:
            dict -- Dict containing keys 'open', 'high', 'low', 'volume', 'last'
        """
        pass

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
        pass
