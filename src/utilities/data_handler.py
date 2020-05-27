import os
import csv
import json

from trades.trade import Trade
from clients.auth_clients.my_authenticated_client import MyAuthenticatedClient

from utilities.utils import getIndexOfCurrency, ISOToUnixTimestamp


class DataHandler():
    def __init__(self, dir_path):
        self.dir_path = dir_path
        os.makedirs(self.dir_path)
        self.trade_history = None
        self.trade_history_filename = self.dir_path + "/trade_history.csv"
        self.trade_history_columns = \
            ['timestamp', 'id', 'product_id', 'side', 'funds',
                'specified_funds', 'executed_value', 'filled_size', 'type',
                'created_at', 'done_at', 'fill_fees', 'status', 'settled']

        with open(self.trade_history_filename, 'a') as csvfile:
            self.trade_writer = csv.DictWriter(
                csvfile,
                fieldnames=self.trade_history_columns,
                restval='n/a',
                extrasaction='ignore')
            self.trade_writer.writeheader()

        self.balance_history = None
        self.balance_history_filename = self.dir_path + "/balance_history.csv"
        self.balance_history_columns = \
            ['timestamp', 'id', 'currency', 'balance', 'available']

        with open(self.balance_history_filename, 'a') as csvfile:
            self.balance_writer = csv.DictWriter(
                csvfile,
                fieldnames=self.balance_history_columns,
                restval='n/a',
                extrasaction='ignore')
            self.balance_writer.writeheader()

        self.config_filename = self.dir_path + "/config.json"

    def write_trade_history(self, data: list):
        """[summary]

        Arguments:
            data {list} -- [description]
        """
        # Filter all dict fields that have one of the desired keys
        # data = {k: data[k] if k in data else 'n/a' for k in self.trade_history_columns}
        try:
            with open(self.trade_history_filename, 'a') as csvfile:
                self.trade_writer = csv.DictWriter(
                    csvfile,
                    fieldnames=self.trade_history_columns,
                    restval='n/a',
                    extrasaction='ignore')
                
                timestamp = ISOToUnixTimestamp(data['done_at'])
                data['timestamp'] = timestamp
                self.trade_writer.writerow(data)
        except IOError:
            print("I/O error on writing trade history")

    def write_balances(
            self, auth_client: MyAuthenticatedClient, products: str):
        """Write all currency balances with timestamp into csv.

        Arguments:
            auth_client {MyAuthenticatedClient} -- [description]
        """
        timestamp = ISOToUnixTimestamp(auth_client.get_time()['iso'])  # Unix epoch
        accounts = auth_client.get_accounts()

        currency_indices = [
            getIndexOfCurrency(accounts, products[:3]),
            getIndexOfCurrency(accounts, products[-3:])]

        try:
            with open(self.balance_history_filename, 'a') as csvfile:
                self.balance_writer = csv.DictWriter(
                        csvfile,
                        fieldnames=self.balance_history_columns,
                        restval='n/a',
                        extrasaction='ignore')
                for idx in currency_indices:
                    accounts[idx]['timestamp'] = timestamp
                    self.balance_writer.writerow(accounts[idx])
        except IOError:
            print("I/O error on writing balance history")

    def write_config(self, config: dict):
        try:
            with open(self.config_filename, 'w') as outfile:
                json.dump(config, outfile, indent=4)
        except IOError:
            print("I/O error on writing balance history")
