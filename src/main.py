import cbpro

from strategies.relative_drop_strategy import RelativeDropStrategy

from signal_generators.buy_signal_generators.relative_drop_signal import RelativeDropSignal
from signal_generators.buy_signal_generators.buy_signal_generator import BuySignalGenerator

from risk_allocators.simple_percentage_risk_allocator import SimplePercentageRiskAllocator

from utilities.secrets import Secrets


product = 'BTC-EUR'

public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(
    Secrets.sandbox_key,
    Secrets.sandbox_b64secret,
    Secrets.sandbox_passphrase,
    api_url="https://api-public.sandbox.pro.coinbase.com")

while True:
    # Spawn N strategies
    # Wait until a strategy returns True, spawn a new one
    strategy = RelativeDropStrategy(product, public_client, auth_client, 0.2)
    strategy.execute()
    print('Strategy done')