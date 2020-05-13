import cbpro

from trades.trade import Trade


class SellTrade(Trade):
    def __init__(self, auth_client: cbpro.AuthenticatedClient, order_type: str, order_side: str, product: str, sell_size: float):
        super(SellTrade, self).__init__(auth_client, order_type, order_side, product)
        self.sell_size = sell_size

    def execute(self):
        self.sell_size = self._round_funds(self.sell_size, self.product[:3])
        if self.order_type == 'market':
            return self.auth_client.sell(
                self.product,
                self.order_type,
                size=self.sell_size
            )
        else:
            raise Exception('Only market orders supported thus far')