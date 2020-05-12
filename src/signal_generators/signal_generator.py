import cbpro

class SignalGenerator():
    def __init__(self, publicClient: cbpro.PublicClient, product: str):
        self.publicClient = publicClient
        self.product = product