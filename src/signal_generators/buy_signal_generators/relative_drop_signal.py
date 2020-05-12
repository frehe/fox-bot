import time
from datetime import datetime, timezone

from signal_generators.buy_signal_generators.buy_signal_generator import BuySignalGenerator


class RelativeDropSignal(BuySignalGenerator):
    def __init__(self, publicClient, product, timespan, drop_percentage, max_price_percentage):
        """[summary]

        Arguments:
            BuySignalGenerator {[type]} -- [description]
            publicClient {[type]} -- [description]
            product {[type]} -- [description]
            timespan {[type]} -- [description]
            drop_percentage {[type]} -- [description]
            max_price_percentage {[type]} -- Buy only if current price is at most low + percentage * (high - low)
        """        
        self.drop_percentage = drop_percentage
        self.max_price_percentage = max_price_percentage
        super(RelativeDropSignal, self).__init__(publicClient, product, timespan)
    
    def getSignal(self):
        while not self.signal:
            timestamp = self.publicClient.get_time()
            current_epoch = timestamp['epoch']
            # current_iso = timestamp['iso']
            past_start_time_iso = datetime.fromtimestamp(current_epoch - self.timespan, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            past_end_time_iso = datetime.fromtimestamp(current_epoch - self.timespan + self.granularity, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            # current_start_time_iso = datetime.fromtimestamp(current_epoch - 2*self.granularity, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            # current_end_time_iso = datetime.fromtimestamp(current_epoch, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

            self.past_rate = self._getRate(past_start_time_iso, past_end_time_iso)

            day_stats = self.publicClient.get_product_24hr_stats(self.product)

            self.current_rate = float(day_stats['last'])
            self.day_low = float(day_stats['low'])
            self.day_high = float(day_stats['high'])

            self.signal = self._relativeDropSignal(self.past_rate, self.current_rate)
            
            time.sleep(self.granularity)
        return True
    
    def _relativeDropSignal(self, past_rate, current_rate) -> bool:
        """Issue a buy signal if relative drop is at least drop percentage

        Arguments:
            past_rate {[type]} -- [description]
            current_rate {[type]} -- [description]
        """
        price_dropped = (1.0 - self.drop_percentage) * self.past_rate > self.current_rate
        price_is_low = self.current_rate < self.day_low + self.max_price_percentage * (self.day_high - self.day_low)
        if price_dropped and price_is_low:
            # Buy signal
            return True
        return False

