import cbpro
import time

from strategies.relative_drop_strategy import RelativeDropStrategy

from utilities.secrets import Secrets

from backtesting.backtest import Backtest


product = 'BTC-EUR'

public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(
    Secrets.sandbox_key,
    Secrets.sandbox_b64secret,
    Secrets.sandbox_passphrase,
    api_url="https://api-public.sandbox.pro.coinbase.com")


a = Backtest('EUR', 'BTC', '2020-02-20T14:00:00.000000', '2020-02-25T14:00:00.000000', 'GDAX')
a.loadPriceData()


# Spawn N strategies
# Wait until a strategy returns True, spawn a new one
strategy = RelativeDropStrategy(product, public_client, auth_client, 0.2)
strategy.execute()
time.sleep(300)
strategy.strategy_active = False  # Gracefully end strategy
print('Strategy done')
