from utilities.my_authenticated_client import MyAuthenticatedClient
from pycoingecko import CoinGeckoAPI

from strategies.strategy import Strategy
from utilities.utils import getIDOfCurrencyCoinGecko, ISOToUnixTimestamp


class Backtest():
    def __init__(
            self, base_currency: str, buy_currency: str,
            start_time: str, end_time: str,
            exchange: str):
        """Initialize backtest.

        Arguments:
            base_currency {str} -- [description]
            buy_currency {str} -- [description]
            start_time {int} -- ISO 8601 
            end_time {int} -- ISO 8601
            exchange {str} -- [description]
        """

        self.time_grid = []
        self.base_currency = base_currency
        self.buy_currency = buy_currency
        self.exchange = exchange

        self.price_data = None
        self.cg = CoinGeckoAPI()

        # Convert start and end dates to epoch
        self.start_epoch = ISOToUnixTimestamp(start_time)
        self.end_epoch = ISOToUnixTimestamp(end_time)

    def loadPriceData(self):
        coins_list = self.cg.get_coins_list()
        buy_currency_id = \
            getIDOfCurrencyCoinGecko(coins_list, self.buy_currency)

        self.price_data = self.cg.get_coin_market_chart_range_by_id(
            id=buy_currency_id,
            vs_currency=self.base_currency.lower(),
            from_timestamp=self.start_epoch,
            to_timestamp=self.end_epoch)['prices']

    def createAnalysis(self, strategy: Strategy):
        """Analyze the performance of a provided strategy.

        Arguments:
            strategy {Strategy} -- The strategy to analyze
        """
        pass
