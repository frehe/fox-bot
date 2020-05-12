import threading
import time
import cbpro
from datetime import datetime, timezone

from signal_generators.signal_generator import SignalGenerator
from utilities.secrets import Secrets
from utilities.my_websocket_client import MyWebsocketClient


class BuySignalGenerator(SignalGenerator):
    def __init__(self, publicClient: cbpro.PublicClient, product: str, timespan: int):
        """Init a signal generator with given parameters.

        A signal generator analyzes past price data. It returns triggers to buy or sell when an event occurs.

        Arguments:
            timespan {int} -- analyze price changes over this number of seconds past.
        """
        super(BuySignalGenerator, self).__init__(publicClient, product)

        self.timespan = timespan
        self.wsClient = None
        self.publicClient = publicClient
        self.product = product

        self.granularity = 60  # {60, 300, 900, 3600, 21600, 86400}
        self.signal = False
    
    def getSignal(self):
        # self.wsClient = MyWebsocketClient(
        #     products=products,
        #     auth=True,
        #     api_key=Secrets.key,
        #     api_secret=Secrets.b64secret,
        #     api_passphrase=Secrets.passphrase,
        #     channels=[{ "name": "ticker"}])
        # self.wsClient.start()
        pass
        
        
    def close_subscription(self):
        # if isinstance(self.wsClient, cbpro.WebsocketClient):
        #     self.wsClient.close()
        pass
    
    def _getRate(self, start, end):
        # get price
        print('getting rates')
        rates = self.publicClient.get_product_historic_rates(
            product_id=self.product,
            start=start,
            end=end,
            granularity=self.granularity)
        window_low = rates[0][1]

        return window_low


