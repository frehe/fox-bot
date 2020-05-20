import calendar

from datetime import datetime, timezone


def getIndexOfCurrency(accounts: list, currency: str) -> int:
    return _getIndex(accounts, currency, 'currency')


def getIndexOfOrder(order_list: list, order: str) -> int:
    return _getIndex(order_list, order, 'id')


def getIDOfCurrencyCoinGecko(coins_list: list, currency: str) -> str:
    idx = _getIndex(coins_list, currency.lower(), 'symbol')
    return coins_list[idx]['id']


def getIndexOfClosestEpoch(price_data: list, abs_epoch: int) -> int:
    closest_index = 0
    for i, entry in enumerate(price_data):
        if abs(entry[0] - abs_epoch) < abs(price_data[closest_index][0] - abs_epoch):
            closest_index = i
    return closest_index


def _getIndex(list_of_dicts: list, target_item: str, field: str) -> int:
    return [
        elem[field] for _, elem in enumerate(list_of_dicts)
        ].index(target_item)


def UnixToISOTimestamp(unix_time: float) -> str:
    """Convert the unix epoch time into a ISO8601-formatted date.

    Arguments:
        unix_time {str} -- [description]

    Returns:
        str -- [description]
    """
    return datetime.fromtimestamp(unix_time, tz=timezone.utc)\
        .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def ISOToUnixTimestamp(iso_time: str) -> str:
    """Convert an ISO8601 date into the unix epoch time.

    Arguments:
        iso_time {str} -- formatted as '%Y-%m-%dT%H:%M:%S.%f'

    Returns:
        str -- [description]
    """
    if iso_time[-1] == 'Z':
        iso_time = iso_time[:-1] + '000'

    return str(calendar.timegm(datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%S.%f').timetuple()))
