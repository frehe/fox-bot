from cbpro.authenticated_client import AuthenticatedClient


class MyAuthenticatedClient(AuthenticatedClient):
    def __init__(self, key, b64secret, passphrase, api_url="https://api.pro.coinbase.com"):
        super(MyAuthenticatedClient, self).__init__(
            key, b64secret, passphrase, api_url)
