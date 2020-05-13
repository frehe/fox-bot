from cbpro.public_client import PublicClient


class MyPublicClient(PublicClient):
    def __init__(self, api_url='https://api.pro.coinbase.com', timeout=30):
        super(MyPublicClient, self).__init__(api_url, timeout)