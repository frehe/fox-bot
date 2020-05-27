from abc import ABC


class Signal(ABC):
    def __init__(self):
        self.signal = {
            'activated': False
        }
