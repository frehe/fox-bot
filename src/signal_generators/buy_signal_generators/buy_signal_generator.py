from signal_generators.signal_generator import SignalGenerator
from signals.buy_signal import BuySignal

from clients.public_clients.my_public_client import MyPublicClient


class BuySignalGenerator(SignalGenerator):
    def __init__(
            self, public_client: MyPublicClient, product: str,
            granularity: int, timespan: int):
        """Init a signal generator with given parameters.

        A signal generator analyzes past price data. It returns triggers to
        buy or sell when an event occurs.

        Arguments:
            timespan {int} -- analyze price changes over this number of
                                seconds in the past.
        """
        super(BuySignalGenerator, self).__init__(
            public_client, product, granularity, timespan)

    def getSignal(self) -> BuySignal:
        pass

    def _printStatus(self):
        print('Waiting for buy signal')
