import time

from clients.auth_clients.cbpro_authenticated_client \
    import CBProAuthenticatedClient
from clients.public_clients.cbpro_public_client \
    import CBProPublicClient
from clients.auth_clients.backtesting_authenticated_client \
    import BacktestingAuthenticatedClient
from clients.public_clients.backtesting_public_client \
    import BacktestingPublicClient

from strategies.relative_drop_strategy import RelativeDropStrategy

from utilities.secrets import Secrets


product = 'BTC-EUR'

auth_client = CBProAuthenticatedClient(
    key=Secrets.sandbox_key,
    b64secret=Secrets.sandbox_b64secret,
    passphrase=Secrets.sandbox_passphrase,
    api_url="https://api-public.sandbox.pro.coinbase.com")
public_client = CBProPublicClient()

auth_client = BacktestingAuthenticatedClient()
public_client = BacktestingPublicClient()

# Spawn N strategies
# Wait until a strategy returns True, spawn a new one
strategy = RelativeDropStrategy(product, public_client, auth_client, 0.1)
strategy.backtest(
    '2020-02-20T14:00:00.000000',
    '2020-02-25T14:00:00.000000',
    60,
    {'EUR': 60.0},
    0.005,
    0.005
)
time.sleep(300)
strategy.strategy_active = False  # Gracefully end strategy
print('Strategy done')
