import cbpro

from utilities.secrets import Secrets

public_client = cbpro.PublicClient()
# Sandbox auth client
auth_client = cbpro.AuthenticatedClient(
    Secrets.key,
    Secrets.b64secret,
    Secrets.passphrase,
    api_url="https://api-public.sandbox.pro.coinbase.com")


time = public_client.get_time()
print(time['iso'])
print(auth_client.get_time())