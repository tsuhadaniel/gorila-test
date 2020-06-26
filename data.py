import os

import pandas as pd

import logic


def file_exists(path):
    return os.path.isfile(path)


def load_raw_cdi_prices(path):

    columns = ['dtDate', 'dLastTradePrice']
    cdi_prices = pd.read_csv(path, usecols=columns)
    cdi_prices.columns = ['date', 'price']

    cdi_prices['date'] = pd.to_datetime(cdi_prices['date'], format='%d/%m/%Y')
    cdi_prices = cdi_prices.sort_values(by='date')
    cdi_prices = cdi_prices.reset_index(drop=True)

    return cdi_prices


def save_processed_cdi_prices_file(cdi_data, path):
    cdi_data['cdi_rate'] = cdi_data['cdi_rate'].round(16)
    cdi_data.to_csv(path, index=False)


def create_processed_cdi_prices_file(raw_data_path, processed_data_path):

    cdi_prices = load_raw_cdi_prices(raw_data_path)
    cdi_prices = logic.calculate_cdi_rate_for_time_series(cdi_prices)
    save_processed_cdi_prices_file(cdi_prices, processed_data_path)
    return cdi_prices


def load_processed_cdi_prices_file(path):

    cdi_data = pd.read_csv(path)
    cdi_data['date'] = pd.to_datetime(cdi_data['date'])
    return cdi_data


def initialize_data(raw_data_path='CDI_Prices.csv', processed_data_path='processed_cdi.csv'):

    if file_exists(processed_data_path):
        return load_processed_cdi_prices_file(processed_data_path)

    else:
        return create_processed_cdi_prices_file(raw_data_path, processed_data_path)
