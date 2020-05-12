class Strategy():
    def __init__(self, signal_generator, risk_allocator):
        self.signal_generator = signal_generator
        self.risk_allocator = risk_allocator

    def execute(self):
        # Launch signal generator
        self.signal_generator.getSignal()

        # Allocate a risk value
        self.risk_allocator.