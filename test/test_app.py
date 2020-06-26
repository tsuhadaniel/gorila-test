import unittest

from app import app


class TestApi(unittest.TestCase):


    def setUp(self):

        app.config['TESTING'] = True

        self.expected = '''[
            {"date":"2016-11-14","unitPrice":1000.53396},
            {"date":"2016-11-16","unitPrice":1001.06821},
            {"date":"2016-11-17","unitPrice":1001.60275},
            {"date":"2016-11-18","unitPrice":1002.13757},
            {"date":"2016-11-21","unitPrice":1002.67267},
            {"date":"2016-11-22","unitPrice":1003.20806},
            {"date":"2016-11-23","unitPrice":1003.74374},
            {"date":"2016-11-24","unitPrice":1004.2797},
            {"date":"2016-11-25","unitPrice":1004.81595},
            {"date":"2016-11-28","unitPrice":1005.35249},
            {"date":"2016-11-29","unitPrice":1005.88931},
            {"date":"2016-11-30","unitPrice":1006.42642},
            {"date":"2016-12-01","unitPrice":1006.95472},
            {"date":"2016-12-02","unitPrice":1007.48331},
            {"date":"2016-12-05","unitPrice":1008.01217},
            {"date":"2016-12-06","unitPrice":1008.54131},
            {"date":"2016-12-07","unitPrice":1009.07072},
            {"date":"2016-12-08","unitPrice":1009.60042},
            {"date":"2016-12-09","unitPrice":1010.13039},
            {"date":"2016-12-12","unitPrice":1010.66064},
            {"date":"2016-12-13","unitPrice":1011.19117},
            {"date":"2016-12-14","unitPrice":1011.72198},
            {"date":"2016-12-15","unitPrice":1012.25307},
            {"date":"2016-12-16","unitPrice":1012.78443},
            {"date":"2016-12-19","unitPrice":1013.31607},
            {"date":"2016-12-20","unitPrice":1013.848},
            {"date":"2016-12-21","unitPrice":1014.3802},
            {"date":"2016-12-22","unitPrice":1014.91268},
            {"date":"2016-12-23","unitPrice":1015.44544}
        ]'''.replace('\n', '').replace(' ', '')


    def test_get(self):

        with app.test_client() as client:
            response = client.get('/api?investmentDate=2016-11-14&currentDate=2016-12-26&cdbRate=103.5')
            result = response.data.decode('utf-8')

            self.assertEqual(self.expected, result)
            self.assertEqual(200, response.status_code)


    def test_get_exception(self):

        expected = '{"error": "x is not a valid number."}'

        with app.test_client() as client:
            response = client.get('/api?investmentDate=2016-11-14&currentDate=2016-12-26&cdbRate=x')
            result = response.data.decode('utf-8')

            self.assertEqual(expected, result)
            self.assertEqual(400, response.status_code)


    def test_post(self):

        input_example = '''{
	        "investmentDate":"2016-11-14",
            "cdbRate": 103.5,
            "currentDate":"2016-12-26"
        }'''

        with app.test_client() as client:
            response = client.post('/api', data=input_example, content_type='application/json')
            result = response.data.decode('utf-8')

            self.assertEqual(self.expected, result)
            self.assertEqual(200, response.status_code)


    def test_post_exception(self):

        expected = '{"error": "Investment date is out of valid range."}'

        input_example = '''{
	        "investmentDate":"2000-11-14",
            "cdbRate": 103.5,
            "currentDate":"2016-12-26"
        }'''

        with app.test_client() as client:
            response = client.post('/api', data=input_example, content_type='application/json')
            result = response.data.decode('utf-8')

            self.assertEqual(expected, result)
            self.assertEqual(400, response.status_code)
