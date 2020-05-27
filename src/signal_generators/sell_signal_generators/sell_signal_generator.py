from clients.public_clients.my_public_client import MyPublicClient

from signals.buy_signal import BuySignal
from signals.sell_signal import SellSignal

from signal_generators.signal_generator import SignalGenerator


class SellSignalGenerator(SignalGenerator):
    def __init__(
            self, public_client: MyPublicClient, product: str, granularity):
        """Init a signal generator with given parameters.

        A signal generator analyzes past price data. It returns triggers to
        buy or sell when an event occurs.

        Arguments:
            timespan {int} -- analyze price changes over this number of
            seconds past.
        """
        super(SellSignalGenerator, self).__init__(
            public_client, product, granularity)

    def getSignal(self, buy_signal: BuySignal) -> SellSignal:
        pass

    def _printStatus(self):
        print('Waiting for sell signal')
