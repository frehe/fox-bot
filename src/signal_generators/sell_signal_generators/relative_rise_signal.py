from signals.buy_signal import BuySignal
from signals.sell_signal import SellSignal

from signal_generators.sell_signal_generators.sell_signal_generator \
    import SellSignalGenerator

from utilities.secrets import Secrets
from clients.websocket_clients.my_websocket_client import MyWebsocketClient


class RelativeRiseSignal(SellSignalGenerator):
    def __init__(self, public_client, product, granularity, rise_percentage):
        """[summary]

        Arguments:
            BuySignalGenerator {[type]} -- [description]
            public_client {[type]} -- [description]
            product {[type]} -- [description]
            timespan {[type]} -- [description]
            drop_percentage {[type]} -- [description]
            max_price_percentage {[type]} -- Buy only if current price is at
                                        most low + percentage * (high - low)
        """
        super(RelativeRiseSignal, self).__init__(
            public_client, product, granularity)

        self.rise_percentage = rise_percentage
        self.granularity = granularity

        self.wsClient = MyWebsocketClient(
            products=product,
            auth=True,
            api_key=Secrets.key,
            api_secret=Secrets.b64secret,
            api_passphrase=Secrets.passphrase,
            channels=[{"name": "ticker"}])

    def getSignal(self, buy_signal: BuySignal) -> SellSignal:
        self._printStatus()
        # TODO: replace below by info from trade log
        self.buy_rate = buy_signal.signal['current_rate']
        signal = False

        # TODO: replace with standard price queries as with buy-signals
        while not signal:
            self.timestamp = self.public_client.get_time()

            day_stats = self.public_client.get_product_24hr_stats(self.product)

            self.current_rate = float(day_stats['last'])
            self.day_low = float(day_stats['low'])
            self.day_high = float(day_stats['high'])

            signal = self._relativeRiseSignal()

            self.public_client.advance_time(self.granularity)

        sell_signal = SellSignal()
        sell_signal.signal['activated'] = True
        sell_signal.signal['buy_rate'] = self.buy_rate
        sell_signal.signal['current_rate'] = self.current_rate

        return sell_signal

    def _relativeRiseSignal(self) -> bool:
        price_rose = \
            self.current_rate > (1.0 + self.rise_percentage) * self.buy_rate

        print(
            '------\n'
            + self.timestamp['iso']
            + '\nBought at rate: '
            + str(self.buy_rate)
            + '\nCurrent rate: '
            + str(self.current_rate))

        if price_rose:
            print('Prices have risen back up')
            return True
        else:
            print('Prices have not risen back up')
        # return True
        # TODO: Remove above statement
        return False

    def _getRate(self, start, end):
        # get price
        print('Getting rates...')
        rates = self.public_client.get_product_historic_rates(
            product=self.product,
            start=start,
            end=end,
            granularity=self.granularity)
        window_low = rates[0][1]

        return window_low
