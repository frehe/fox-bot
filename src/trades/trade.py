import cbpro
import math
import string
import time

from abc import ABC, abstractmethod
from utilities.product_infos import ProductInfos

class Trade(ABC):
    def __init__(self, auth_client: cbpro.AuthenticatedClient, order_type: str, order_side: str, product: str):
        super().__init__()
        self.auth_client = auth_client
        self.order_type = order_type  # "limit" (="maker") or "market" (="taker")
        self.order_side = order_side  # "buy" or "sell"
        self.product = product  # e.g. "BTC-EUR"
        self.trade_info = None

    def _round_funds(self, funds: float, currency: str) -> float:
        min_amount = float(ProductInfos.min_sizes[currency])
        factor = 1.0 / min_amount
        return math.floor(funds * factor) / round(factor)

    def _waitUntilSettled(self):
        if 'settled' in self.trade_info:
            while self.trade_info['settled'] is not True:
                print('Waiting for trade to settle')
                time.sleep(1)
                self.trade_info = self.auth_client.get_order(self.trade_info['id'])
        else:
            print(self.trade_info)
            if self.trade_info['message'] == 'ServiceUnavailable':
                print('Waiting until service available')
                time.sleep(10)
                self._waitUntilSettled()
            else:
                raise Exception('Trade could not be completed.')
