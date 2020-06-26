import unittest

import pandas as pd

from test import util
import logic


class TestCdiRateFormula(unittest.TestCase):


    def test_for_valid_value_1(self):

        expected = 0.00051591
        result = logic.cdi_rate_formula(13.88)

        self.assertAlmostEqual(expected, result)


    def test_for_valid_value_2(self):

        expected = 0.00050718
        result = logic.cdi_rate_formula(13.63)

        self.assertAlmostEqual(expected, result)


class TestCalculateCdiRateForTimeSeries(unittest.TestCase):


    def test(self):

        expected = util.matrix_to_dataframe([
            ['2019-11-27', 13.88, 0.0005159071471232402],
            ['2019-11-28', 13.63, 0.000507181628455422]
        ])

        input_example = util.matrix_to_dataframe([
            ['2019-11-27', 13.88],
            ['2019-11-28', 13.63]
        ])
        result = logic.calculate_cdi_rate_for_time_series(input_example)

        pd.testing.assert_frame_equal(expected, result)


class TestFilterByDateInterval(unittest.TestCase):


    def setUp(self):
        input_example = [
            ['2020-12-01', 1, 10],
            ['2020-12-02', 2, 20],
            ['2020-12-03', 3, 30],
            ['2020-12-04', 4, 40],
            ['2020-12-05', 5, 50],
            ['2020-12-06', 6, 60],
            ['2020-12-07', 7, 70],
            ['2020-12-08', 8, 80],
            ['2020-12-09', 9, 90],
        ]

        self.input_example = util.matrix_to_dataframe(input_example)


    def test_for_valid_interval(self):

        expected = util.matrix_to_dataframe([
            ['2020-12-04', 4, 40],
            ['2020-12-05', 5, 50],
            ['2020-12-06', 6, 60],
        ])

        start = util.str_to_datetime('2020-12-04')
        end = util.str_to_datetime('2020-12-07')

        result = logic.filter_by_date_interval(self.input_example, start, end)
        result = result.reset_index(drop=True)

        pd.testing.assert_frame_equal(expected, result)


    def test_for_full_range(self):

        expected = self.input_example

        start = util.str_to_datetime('2020-12-01')
        end = util.str_to_datetime('2020-12-10')

        result = logic.filter_by_date_interval(self.input_example, start, end)
        result = result.reset_index(drop=True)

        pd.testing.assert_frame_equal(expected, result)


    def test_for_last_days(self):

        expected = util.matrix_to_dataframe([
            ['2020-12-09', 9, 90],
        ])

        start = util.str_to_datetime('2020-12-09')
        end = util.str_to_datetime('2020-12-10')

        result = logic.filter_by_date_interval(self.input_example, start, end)
        result = result.reset_index(drop=True)

        pd.testing.assert_frame_equal(expected, result)


    def test_when_start_is_bigger_than_end(self):

        start = util.str_to_datetime('2020-12-07')
        end = util.str_to_datetime('2020-12-04')

        with self.assertRaises(ValueError):
            logic.filter_by_date_interval(self.input_example, start, end)


    def test_when_start_is_equalls_end(self):

        start = util.str_to_datetime('2020-12-07')
        end = util.str_to_datetime('2020-12-07')

        with self.assertRaises(ValueError):
            logic.filter_by_date_interval(self.input_example, start, end)


    def test_when_start_and_end_are_out_of_range(self):

        start = util.str_to_datetime('2020-11-30')
        end = util.str_to_datetime('2020-12-11')

        with self.assertRaises(ValueError):
            logic.filter_by_date_interval(self.input_example, start, end)


    def test_when_start_is_out_of_range(self):

        start = util.str_to_datetime('2020-11-30')
        end = util.str_to_datetime('2020-12-09')

        with self.assertRaises(ValueError):
            logic.filter_by_date_interval(self.input_example, start, end)


    def test_when_end_is_out_of_range(self):

        start = util.str_to_datetime('2020-12-01')
        end = util.str_to_datetime('2020-12-11')

        with self.assertRaises(ValueError):
            logic.filter_by_date_interval(self.input_example, start, end)


class TestCdiPartialRate(unittest.TestCase):


    def test_for_valid_value(self):

        expected = 1.0005339668500000

        cdb = 103.5
        cdi_rate = 0.00051591
        result = logic.cdi_partial_rate(cdi_rate, cdb)

        self.assertEqual(expected, result)


class TestCalculateAccumulatedCdiRate(unittest.TestCase):


    def setUp(self):
        input_example = [
            ['2020-12-01', 13.88, 0.00051591],
            ['2020-12-02', 13.88, 0.00051591],
            ['2020-12-03', 13.88, 0.00051591],
            ['2020-12-04', 13.88, 0.00051591],
            ['2020-12-05', 13.88, 0.00051591],
            ['2020-12-06', 13.88, 0.00051591],
            ['2020-12-07', 13.88, 0.00051591],
            ['2020-12-08', 13.88, 0.00051591],
            ['2020-12-09', 13.88, 0.00051591],
        ]
        self.input_example = util.matrix_to_dataframe(input_example)


    def test_if_accumulated_values_are_correct(self):

        expected = util.matrix_to_dataframe([
            ['2020-12-01', 1.0005339668500000],
            ['2020-12-02', 1.0010682188206000],
            ['2020-12-03', 1.0016027560640400],
            ['2020-12-04', 1.0021375787326500],
            ['2020-12-05', 1.0026726869788300],
            ['2020-12-06', 1.0032080809550800],
            ['2020-12-07', 1.0037437608139600],
            ['2020-12-08', 1.0042797267081300],
            ['2020-12-09', 1.0048159787903200],
        ], ['date', 'accumulated'])

        cdb = 103.5

        result = logic.calculate_accumulated_cdi_rate(self.input_example, cdb)

        pd.testing.assert_frame_equal(expected, result)


class TestCalculateCdbForPeriod(unittest.TestCase):


    def setUp(self):
        input_example = [
            ['2020-12-01', 13.88, 0.00051591],
            ['2020-12-02', 13.88, 0.00051591],
            ['2020-12-03', 13.88, 0.00051591],
            ['2020-12-04', 13.88, 0.00051591],
            ['2020-12-05', 13.88, 0.00051591],
            ['2020-12-06', 13.88, 0.00051591],
            ['2020-12-07', 13.88, 0.00051591],
            ['2020-12-08', 13.88, 0.00051591],
            ['2020-12-09', 13.88, 0.00051591],
        ]
        self.input_example = util.matrix_to_dataframe(input_example)


    def test_if_values_are_correct(self):

        expected = pd.DataFrame([
            ['2020-12-01', 1000.533966],
            ['2020-12-02', 1001.068218],
            ['2020-12-03', 1001.602756],
            ['2020-12-04', 1002.137578],
            ['2020-12-05', 1002.672686],
            ['2020-12-06', 1003.208080],
            ['2020-12-07', 1003.743760],
            ['2020-12-08', 1004.279726],
            ['2020-12-09', 1004.815978],
        ], columns = ['date', 'unitPrice'])

        cdb = 103.5
        start = util.str_to_datetime('2020-12-01')
        end = util.str_to_datetime('2020-12-10')

        result = logic.calculate_cdb_for_period(self.input_example, cdb, start, end)

        pd.testing.assert_frame_equal(expected, result)
