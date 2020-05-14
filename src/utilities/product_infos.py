from utilities.my_public_client import MyPublicClient


class ProductInfos():
    min_sizes = {}

    @staticmethod
    def refresh(public_client: MyPublicClient, product: str):
        buy_currency = product[:3]
        base_currency = product[-3:]

        currencies = public_client.get_currencies()
        currency_list = [elem['id'] for _, elem in enumerate(currencies)]

        ProductInfos.min_sizes[buy_currency] = currencies[currency_list.index(buy_currency)]['min_size']
        ProductInfos.min_sizes[base_currency] = currencies[currency_list.index(base_currency)]['min_size']
