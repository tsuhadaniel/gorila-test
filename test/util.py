from datetime import datetime

import pandas as pd


def str_to_datetime(value):
    return datetime.strptime(value, '%Y-%m-%d')


def matrix_to_dataframe(data, columns=[]):

    if len(columns) == 0:

        columns = ['date', 'price', 'cdi_rate', 'accumulated']

        if len(data[0]) == 3:
            columns = ['date', 'price', 'cdi_rate']

        elif len(data[0]) == 2:
            columns = ['date', 'price']

    data = pd.DataFrame(data, columns=columns)
    data['date'] = pd.to_datetime(data['date'])
    data = data.reset_index(drop=True)

    return data