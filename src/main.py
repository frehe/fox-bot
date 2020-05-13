import cbpro

from strategies.relative_drop_strategy import RelativeDropStrategy

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
