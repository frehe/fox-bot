import cbpro

from trades.trade import Trade


class BuyTrade(Trade):
    def __init__(self, auth_client: cbpro.AuthenticatedClient, order_type: str, order_side: str, product: str, use_funds: float):
        super(BuyTrade, self).__init__(auth_client, order_type, order_side, product)
        self.use_funds = use_funds

    def execute(self):
        self.use_funds = self._round_funds(self.use_funds, self.product[-3:])
        if self.order_type == "market":
            self.trade_info = self.auth_client.buy_taker(
                self.product,
                funds=self.use_funds,
            )
            self._waitUntilSettled()
            return self.trade_info
        elif self.order_type == 'limit':
            # TODO
            pass
        else:
            raise Exception('Only market orders supported thus far')