import cbpro

from signals.buy_signal import BuySignal
from signals.sell_signal import SellSignal
from signals.signal import Signal

from trades.buy_trade import BuyTrade
from trades.sell_trade import SellTrade

from risk_allocators.risk_allocator import RiskAllocator


class SimplePercentageRiskAllocator(RiskAllocator):
    def __init__(self, auth_client: cbpro.AuthenticatedClient, product: str, p):
        super(SimplePercentageRiskAllocator, self).__init__(auth_client, product)
        self.p = p

    def createBuyTrade(self, buy_signal: BuySignal) -> BuyTrade:
        self.activated = buy_signal.signal['activated']
        # self.current_rate = signal.signal['current_rate']

        self.available_to_sell = self._getAvailableSell()
        use_funds = self.available_to_sell

        if self.activated:
            trade = BuyTrade(self.auth_client, 'market', 'buy', self.product, use_funds)
        else:
            raise ValueError("Buy signal is not activated")
            
        return trade

    def createSellTrade(self, sell_signal: SellSignal) -> SellTrade:
        self.activated = sell_signal.signal['activated']

        self.available_to_sell = self._getAvailableBuy()
        sell_funds = self.available_to_sell

        if self.activated:
            trade = SellTrade(self.auth_client, 'market', 'sell', self.product, sell_funds)
        else:
            raise ValueError("Sell signal is not activated")

        return trade

    def _extractFromSignal(self, signal: Signal):
        pass

    def _getAvailableBuy(self):
        accounts = self.auth_client.get_accounts()
        buy_currency = self.product[:3]
        buy_index = [elem['currency'] for _, elem in enumerate(accounts)].index(buy_currency)

        return float(accounts[buy_index]['available'])

    def _getAvailableSell(self):
        accounts = self.auth_client.get_accounts()
        sell_currency = self.product[-3:]
        sell_index = [elem['currency'] for _, elem in enumerate(accounts)].index(sell_currency)

        return float(accounts[sell_index]['available'])
