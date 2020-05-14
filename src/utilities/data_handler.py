import os
import csv

from trades.trade import Trade

class DataHandler():
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.trade_history = None
        self.trade_history_filename = self.dir_path + "trade_history.csv"
        self.trade_history_columns = \
            ['id', 'product_id', 'side', 'funds', 'specified_funds',
                'executed_value', 'filled_size', 'type', 'created_at',
                'done_at', 'fill_fees', 'status', 'settled']

    def write_trade_history(self, data: list):
        # Filter all dict fields that have one of the desired keys
        data = {k: data[k] for k in self.trade_history_columns}
        try:
            with open(self.trade_history_filename, 'w') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=self.trade_history_columns)
                writer.writeheader()
                for d in data.values():
                    writer.writerow(d)
        except IOError:
            print("I/O error on writing trade history")

    def write_holdings(self):
        pass
