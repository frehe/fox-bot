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
        drop_percentage = config['strategy_params']['drop_percentage']
        rise_percentage = config['strategy_params']['rise_percentage']
        granularity = config['strategy_params']['granularity']
        timespan = config['strategy_params']['timespan']
        max_price_percentage = \
            config['strategy_params']['max_price_percentage']

        buy_signal_generator = \
            RelativeDropSignal(
                public_client, product, timespan,
                granularity, drop_percentage, max_price_percentage)
        sell_signal_generator = \
            RelativeRiseSignal(
                public_client, product, granularity, rise_percentage)
        risk_allocator = \
            SimplePercentageRiskAllocator(auth_client, product, 1.0)

        super(RelativeDropStrategy, self).__init__(
            buy_signal_generator,
            sell_signal_generator,
            risk_allocator,
            product,
            public_client,
            auth_client,
            config)
