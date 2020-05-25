from signal_generators.buy_signal_generators.buy_signal_generator import BuySignalGenerator
from signals.buy_signal import BuySignal

from utilities.utils import UnixToISOTimestamp


class RelativeDropSignal(BuySignalGenerator):
    def __init__(self, public_client, product, timespan, drop_percentage, max_price_percentage):
        """[summary]

        Arguments:
            BuySignalGenerator {[type]} -- [description]
            public_client {[type]} -- [description]
            product {[type]} -- [description]
            timespan {[type]} -- [description]
            drop_percentage {[type]} -- [description]
            max_price_percentage {[type]} -- Buy only if current price is at most low + percentage * (high - low)
        """
        self.drop_percentage = drop_percentage
        self.max_price_percentage = max_price_percentage
        self.granularity = 3600  # {60, 300, 900, 3600, 21600, 86400}
        super(RelativeDropSignal, self).__init__(
            public_client, product, timespan)

    def getSignal(self) -> BuySignal:
        self._printStatus()
        signal = False
        
        while not signal:
            self.timestamp = self.public_client.get_time()
            current_epoch = self.timestamp['epoch']

            past_start_time_iso = UnixToISOTimestamp(current_epoch - self.timespan)
            past_end_time_iso = UnixToISOTimestamp(current_epoch - self.timespan + self.granularity)

            self.past_rate = self._getRate(past_start_time_iso, past_end_time_iso)

            day_stats = self.public_client.get_product_24hr_stats(self.product)

            self.current_rate = float(day_stats['last'])
            self.day_low = float(day_stats['low'])
            self.day_high = float(day_stats['high'])

            signal = self._relativeDropSignal()

            self.public_client.advance_time(self.granularity)

        buy_signal = BuySignal()
        buy_signal.signal['activated'] = True
        buy_signal.signal['past_rate'] = self.past_rate
        buy_signal.signal['current_rate'] = self.current_rate
        return buy_signal

    def _relativeDropSignal(self) -> bool:
        """Issue a buy signal if relative drop is at least drop percentage

        Arguments:
            past_rate {[type]} -- [description]
            current_rate {[type]} -- [description]
        """
        price_dropped = (1.0 - self.drop_percentage) * self.past_rate > self.current_rate
        price_is_low = self.current_rate < self.day_low + self.max_price_percentage * (self.day_high - self.day_low)

        print('------'+ self.timestamp['iso'] + '\nPast rate: ' + str(self.past_rate) + '\nCurrent rate: ' + str(self.current_rate))

        if price_dropped and price_is_low:
            print('Prices have dropped')
            return True
        else:
            print('Prices have not dropped')
        # return True
        # TODO: Remove above statement
        return False

    def _getRate(self, start, end):
        # get price
        print('getting rates')
        rates = self.public_client.get_product_historic_rates(
            product=self.product,
            start=start,
            end=end,
            granularity=self.granularity)
        window_low = rates[0][1]

        return window_low

