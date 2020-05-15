import threading
import time
import cbpro
from datetime import datetime, timezone
from abc import ABC

from signal_generators.signal_generator import SignalGenerator
from signals.buy_signal import BuySignal
from utilities.secrets import Secrets
from clients.my_websocket_client import MyWebsocketClient


class BuySignalGenerator(SignalGenerator):
    def __init__(self, public_client: cbpro.PublicClient, product: str, timespan: int):
        """Init a signal generator with given parameters.

        A signal generator analyzes past price data. It returns triggers to buy or sell when an event occurs.

        Arguments:
            timespan {int} -- analyze price changes over this number of seconds past.
        """
        super(BuySignalGenerator, self).__init__(public_client, product, timespan)
    
    def getSignal(self) -> BuySignal:
        pass

    def _printStatus(self):
        print('Waiting for buy signal')


