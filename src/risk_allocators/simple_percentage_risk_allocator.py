import cbpro


from risk_allocators.risk_allocator import RiskAllocator


class SimplePercentageRiskAllocator(RiskAllocator):
    def __init__(self, authClient: cbpro.AuthenticatedClient, product: str, p):
        super(SimplePercentageRiskAllocator, self).__init__(authClient, product)
        self.p = p