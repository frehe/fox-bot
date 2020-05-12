from strategies.strategy import Strategy

class RelativeDropStrategy(Strategy):
    def __init__(self, signal_generator, risk_allocator):
        """Initialize the relative drop strategy

        Arguments:
            Strategy {Strategy} -- A general template for any trading strategy
            signal_generator {SignalGenerator} -- A specific signal generator
            risk_allocator {RiskAllocator} -- A specific risk allocator
        """
        super(RelativeDropStrategy, self).__init__(signal_generator, risk_allocator)
    
    def run_strategy(self):
        pass