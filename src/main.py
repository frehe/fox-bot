import time
import json
import argparse

from clients.auth_clients.cbpro_authenticated_client \
    import CBProAuthenticatedClient
from clients.public_clients.cbpro_public_client \
    import CBProPublicClient
from clients.auth_clients.backtesting_authenticated_client \
    import BacktestingAuthenticatedClient
from clients.public_clients.backtesting_public_client \
    import BacktestingPublicClient

from strategies.relative_drop_strategy import RelativeDropStrategy

from utilities.utils import getWorkingDirectory, joinPaths
from utilities.secrets import Secrets


def main(args):
    # Read config file
    config_file = joinPaths([getWorkingDirectory(), 'resources', 'config_files', args.input])
    with open(config_file) as cf:
        data = json.load(cf)

    product = data['product']

    if args.backtest:
        auth_client = BacktestingAuthenticatedClient()
        public_client = BacktestingPublicClient()
    else:
        exchange = data['Exchange']
        if exchange == "Coinbase Pro":
            auth_client = CBProAuthenticatedClient(
                key=Secrets.sandbox_key,
                b64secret=Secrets.sandbox_b64secret,
                passphrase=Secrets.sandbox_passphrase,
                api_url="https://api-public.sandbox.pro.coinbase.com")
            public_client = CBProPublicClient()
        else:
            raise ValueError("Exchange name unknown")

    # Spawn N strategies
    # Wait until a strategy returns True, spawn a new one
    strategy_name = data['strategy']
    if strategy_name == "Relative Drop":
        strategy = RelativeDropStrategy(product, public_client, auth_client, 0.05)
    else:
        raise ValueError("Strategy name unknown")

    if args.backtest:
        print("Backtesting strategy...")
        strategy.backtest(
            data['backtest']['start'],
            data['backtest']['end'],
            data['backtest']['granularity'],
            data['backtest']['start_balances'],
            data['backtest']['maker_fee'],
            data['backtest']['taker_fee']
        )
    else:
        print("Executing strategy...")
        strategy.execute()

    time.sleep(300)
    strategy.strategy_active = False  # Gracefully end strategy
    print('Strategy done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execte a trading strategy with Fox Bot')
    parser.add_argument('-i', '--input', help='a .json input configuration file')
    parser.add_argument(
        '-b', '--backtest', dest='backtest', action='store_true',
        help='if flag is set, backtest the strategy instead of running it')
    parser.add_argument(
        '-v', '--verbose', dest='verbose', action='store_true',
        help='enter verbose mode')
    args = parser.parse_args()
    # ... do something with args.output ...
    # ... do something with args.verbose ..
    main(args)
