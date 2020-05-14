import time
from datetime import datetime, timezone

from signals.buy_signal import BuySignal
from signals.sell_signal import SellSignal

from signal_generators.sell_signal_generators.sell_signal_generator import SellSignalGenerator

from utilities.secrets import Secrets
from utilities.my_websocket_client import MyWebsocketClient


class RelativeRiseSignal(SellSignalGenerator):
    def __init__(self, public_client, product, rise_percentage):
        """[summary]

        Arguments:
            BuySignalGenerator {[type]} -- [description]
            public_client {[type]} -- [description]
            product {[type]} -- [description]
            timespan {[type]} -- [description]
            drop_percentage {[type]} -- [description]
            max_price_percentage {[type]} -- Buy only if current price is at most low + percentage * (high - low)
        """        
        super(RelativeRiseSignal, self).__init__(public_client, product)

        self.rise_percentage = rise_percentage
        self.granularity = 1

        self.wsClient = MyWebsocketClient(
            products=product,
            auth=True,
            api_key=Secrets.key,
            api_secret=Secrets.b64secret,
            api_passphrase=Secrets.passphrase,
            channels=[{"name": "ticker"}])

    def getSignal(self, buy_signal: BuySignal) -> SellSignal:
        self._printStatus()
        self.buy_rate = buy_signal.signal['current_rate']  # TODO: replace by info from trade log

        self.wsClient.start()
        while not self.signal:
            # Get current price from websocket
            self.current_rate = self.wsClient.latest_msg
            if self.current_rate is not None:
                self.signal = self._relativeRiseSignal()
            
            time.sleep(self.granularity)
        
        self.wsClient.close()
        sell_signal = SellSignal()
        sell_signal.signal['activated'] = True

        return sell_signal

    def _relativeRiseSignal(self) -> bool:
        price_rose = self.current_rate > (1.0 + self.rise_percentage) * self.buy_rate

        print('------\nCurrent rate: ' + str(self.current_rate) + '\nBought at rate: ' + str(self.buy_rate))

        if price_rose:
            print('Prices have risen back up')
            return True
        else:
            print('Prices have not risen back up')
        return True
        # TODO: Remove above statement
        return False