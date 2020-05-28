from clients.auth_clients.my_authenticated_client import MyAuthenticatedClient

from signals.buy_signal import BuySignal
from signals.sell_signal import SellSignal
from signals.signal import Signal

from trades.buy_trade import BuyTrade
from trades.sell_trade import SellTrade

from risk_allocators.risk_allocator import RiskAllocator
from utilities.utils import getIndexOfCurrency


class SimplePercentageRiskAllocator(RiskAllocator):
    def __init__(self, auth_client: MyAuthenticatedClient, product: str, p):
        super(SimplePercentageRiskAllocator, self).__init__(
            auth_client, product)
        self.p = p

    def createBuyTrade(self, buy_signal: BuySignal) -> BuyTrade:
        self.activated = buy_signal.signal['activated']
        # self.current_rate = signal.signal['current_rate']

        self.available_to_sell = self._getAvailableSell()
        use_funds = self.p * self.available_to_sell

        if self.activated:
            trade = BuyTrade(
                self.auth_client, 'market', 'buy', self.product, use_funds)
        else:
            raise ValueError("Buy signal is not activated")

        return trade

    def createSellTrade(self, sell_signal: SellSignal) -> SellTrade:
        self.activated = sell_signal.signal['activated']

        self.available_to_sell = self._getAvailableBuy()
        sell_funds = self.available_to_sell

        if self.activated:
            trade = SellTrade(
                self.auth_client, 'market', 'sell', self.product, sell_funds)
        else:
            raise ValueError("Sell signal is not activated")

        return trade

    def _extractFromSignal(self, signal: Signal):
        pass

    def _getAvailableBuy(self):
        accounts = self.auth_client.get_accounts()
        buy_currency = self.product[:3]
        idx = getIndexOfCurrency(accounts, buy_currency)

        return float(accounts[idx]['available'])

    def _getAvailableSell(self):
        accounts = self.auth_client.get_accounts()
        sell_currency = self.product[-3:]
        idx = getIndexOfCurrency(accounts, sell_currency)

        return float(accounts[idx]['available'])
