import os

from flask import Flask, render_template, request, Response, json
import pandas as pd

import data
import logic
import validator


app = Flask(__name__)
app.secret_key = os.urandom(24)

cdi_data = data.initialize_data()


@app.route('/')
def chart():
    return render_template('chart.html')


@app.route('/api', methods=["GET", "POST"])
def api():

    try:
        input_data = request.json if request.method == 'POST' else request.args

        start, end, cdb = validator.validate_request(input_data)
        result = logic.calculate_cdb_for_period(cdi_data, cdb, start, end)

        response = result.to_json(orient='records')
        return Response(response, mimetype='application/json')

    except ValueError as ex:
        response = '{{"error": "{}"}}'.format(ex)
        return (Response(response, mimetype='application/json'), 400)

    except Exception as ex:
        print(ex)
        response = '{ "error": "Unknow error." }'
        return (Response(response, mimetype='application/json'), 500)


@app.route('/health-check')
def health_check():
    response = '{ "status": "ok" }'
    return Response(response, mimetype='application/json')


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)
