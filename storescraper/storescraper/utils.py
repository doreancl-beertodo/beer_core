import importlib
import math
from decimal import Decimal

import requests


def get_store_class_by_name(store_class_name):
    store_module = importlib.import_module('storescraper.storescraper.stores')
    return getattr(store_module, store_class_name)


def session_with_proxy(extra_args):
    session = requests.Session()

    if extra_args and 'proxy' in extra_args:
        proxy = extra_args['proxy']

        session.proxies = {
            'http': proxy,
            'https': proxy,
        }

    return session

def check_ean13(ean):
    if not ean or not isinstance(ean, str):
        return False
    if len(ean) != 13:
        return False
    try:
        int(ean)
    except Exception:
        return False
    oddsum = 0
    evensum = 0
    eanvalue = ean
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10

    if check != int(ean[-1]):
        return False
    return True

def format_currency(value, curr='', sep='.', dp=',',
                    pos='', neg='-', trailneg='', places=0):
    """Convert Decimal to a money formatted string.

    curr: optional currency symbol before the sign (may be blank)
    sep: optional grouping separator (comma, period, space, or blank)
    dp: decimal point indicator (comma or period)
    only specify as blank when places is zero
    pos: optional sign for positive numbers: '+', space or blank
    neg: optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator: '-', ')', space or blank
    places: Number of decimal places to consider
    """

    quantized_precision = Decimal(10) ** -places  # 2 places --> '0.01'
    sign, digits, exp = value.quantize(quantized_precision).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, iter_next = result.append, digits.pop

    if sign:
        build(trailneg)
    for i in range(places):
        build(iter_next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(iter_next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)

    return ''.join(reversed(result))
