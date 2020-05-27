from clients.auth_clients.my_authenticated_client import MyAuthenticatedClient
from clients.public_clients.my_public_client import MyPublicClient

from strategies.strategy import Strategy

from signal_generators.buy_signal_generators \
    .relative_drop_signal import RelativeDropSignal
from signal_generators.sell_signal_generators \
    .relative_rise_signal import RelativeRiseSignal
from risk_allocators.simple_percentage_risk_allocator \
    import SimplePercentageRiskAllocator


class RelativeDropStrategy(Strategy):
    def __init__(
            self, product: str, public_client: MyPublicClient,
            auth_client: MyAuthenticatedClient, config: dict):
        """Initialize the relative drop strategy

        Arguments:
            Strategy {[type]} -- [description]
            product {str} -- [description]
            public_client {MyPublicClient} -- [description]
            auth_client {MyAuthenticatedClient} -- [description]
            config {dict} -- [description]
        """
        p = config['strategy_params']['p']
        granularity = config['strategy_params']['granularity']

        buy_signal_generator = \
            RelativeDropSignal(
                public_client, product, 18*60*60, granularity, p, 0.8)
        sell_signal_generator = \
            RelativeRiseSignal(
                public_client, product, granularity, 0.05)
        risk_allocator = \
            SimplePercentageRiskAllocator(auth_client, product, 0.1)

        super(RelativeDropStrategy, self).__init__(
            buy_signal_generator,
            sell_signal_generator,
            risk_allocator,
            product,
            public_client,
            auth_client,
            config)
