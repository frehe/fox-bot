import cbpro
import math
import string

from abc import ABC, abstractmethod
from utilities.product_infos import ProductInfos

class Trade(ABC):
    def __init__(self, auth_client: cbpro.AuthenticatedClient, order_type: str, order_side: str, product: str):
        super().__init__()
        self.auth_client = auth_client
        self.order_type = order_type  # "limit" (="maker") or "market" (="taker")
        self.order_side = order_side  # "buy" or "sell"
        self.product = product  # e.g. "BTC-EUR"

    def _round_funds(self, funds: float, currency: str) -> float:
        min_amount = float(ProductInfos.min_sizes[currency])
        factor = 1.0 / min_amount
        return math.floor(funds * factor) / round(factor)
        
