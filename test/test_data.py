import os

import unittest
import pandas as pd

from test import util
import data


test_files_dir = os.getcwd() + '/test/'
raw_cdi_prices = test_files_dir + 'CDI_Prices_test.csv'
processed_cdi_prices = test_files_dir + 'processed_cdi_test.csv'


class TestLoadRawCdiPrices(unittest.TestCase):


    def test_for_valid_file(self):

        expected = util.matrix_to_dataframe([
            ['2019-11-27', 5],
            ['2019-11-28', 4],
            ['2019-11-29', 3],
            ['2019-12-02', 2],
            ['2019-12-03', 1]
        ])

        result = data.load_raw_cdi_prices(raw_cdi_prices)

        pd.testing.assert_frame_equal(expected, result)


class TestSaveAndLoadCdiFile(unittest.TestCase):


    def setUp(self):
        if os.path.exists(processed_cdi_prices):
            os.remove(processed_cdi_prices)


    def tearDown(self):
        if os.path.exists(processed_cdi_prices):
            os.remove(processed_cdi_prices)


    def test_save_and_load_file(self):

        expected = util.matrix_to_dataframe([
            ['2019-11-27', 5, 0.0001936305065440],
            ['2019-11-28', 4, 0.0001556498627913],
            ['2019-11-29', 3, 0.0001173037138344],
            ['2019-12-02', 2, 0.0000785849419846],
            ['2019-12-03', 1, 0.0000394862194537]
        ])

        data.save_processed_cdi_prices_file(expected, processed_cdi_prices)

        result = data.load_processed_cdi_prices_file(processed_cdi_prices)

        pd.testing.assert_frame_equal(expected, result)


class TestCreateProcessedCdiPricesFile(unittest.TestCase):


    def setUp(self):
        if os.path.exists(processed_cdi_prices):
            os.remove(processed_cdi_prices)

        expected = [
            ['2019-11-27', 5, 0.0001936305065440],
            ['2019-11-28', 4, 0.0001556498627913],
            ['2019-11-29', 3, 0.0001173037138344],
            ['2019-12-02', 2, 0.0000785849419846],
            ['2019-12-03', 1, 0.0000394862194537]
        ]

        self.expected = util.matrix_to_dataframe(expected)


    def tearDown(self):
        if os.path.exists(processed_cdi_prices):
            os.remove(processed_cdi_prices)


    def test_if_values_are_correct(self):

        result = data.create_processed_cdi_prices_file(raw_cdi_prices, processed_cdi_prices)

        pd.testing.assert_frame_equal(self.expected, result)


    def test_if_file_is_correct(self):

        data.create_processed_cdi_prices_file(raw_cdi_prices, processed_cdi_prices)
        result = data.load_processed_cdi_prices_file(processed_cdi_prices)

        pd.testing.assert_frame_equal(self.expected, result)
