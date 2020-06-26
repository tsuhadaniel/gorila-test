from datetime import datetime
from datetime import timedelta

import pandas as pd


# TCDI
def cdi_rate_formula(cdi):
    base = (cdi/100) + 1
    exponent = (1/252)
    return pow(base, exponent) - 1


def calculate_cdi_rate_for_time_series(cdi_prices):

    cdi_rate = cdi_rate_formula(cdi_prices['price'])
    cdi_prices['cdi_rate'] = cdi_rate
    return cdi_prices


def _validate_intervals(cdi_prices, start, end):

    min = cdi_prices['date'].min()
    max = cdi_prices['date'].max() + timedelta(days=1)

    valid_start = min <= start and start <= max
    valid_end = min <= end and end <= max

    if start >= end:
        raise ValueError('Investment date must be strictly greater than current date.')

    if not valid_start and not valid_end:
        raise ValueError('Investment date and current date are out of valid range.')

    if not valid_start:
        raise ValueError('Investment date is out of valid range.')

    if not valid_end:
        raise ValueError('Current date is out of valid range.')


def filter_by_date_interval(cdi_prices, start, end):

    _validate_intervals(cdi_prices, start, end)

    filter = (start <= cdi_prices['date']) & (cdi_prices['date'] < end)
    return cdi_prices.loc[filter]


# TCDI Acumulado (Termo)
def cdi_partial_rate(cdi, cdb):
    return 1 + cdi * cdb/100


def calculate_accumulated_cdi_rate(cdi_prices, cdb_rate):

    accumulated = cdi_partial_rate(cdi_prices['cdi_rate'], cdb_rate)
    accumulated = accumulated.cumprod()

    result = pd.DataFrame()
    result['date'] = cdi_prices['date']
    result['accumulated'] = accumulated

    return result


def calculate_cdb_for_period(cdi_data, cdb_rate, start, end):

    cdb_unit_price = 1000

    interval = filter_by_date_interval(cdi_data, start, end)

    accumulated = calculate_accumulated_cdi_rate(interval, cdb_rate)
    accumulated['accumulated'] = round(accumulated['accumulated'], 8)
    accumulated['accumulated'] = accumulated['accumulated'] * cdb_unit_price

    result = pd.DataFrame()
    result['date'] = accumulated['date'].dt.strftime('%Y-%m-%d')
    result['unitPrice'] = accumulated['accumulated']

    return result
