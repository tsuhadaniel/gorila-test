from datetime import datetime


def _get_parameter(request, parameter):

    if request[parameter]:
        return request[parameter]
    else:
        raise ValueError('{} is a required parameter.'.format(parameter))


def _parse_date_format(value):

    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise ValueError('{} is not a valid date format.'.format(value))


def _parse_float(value):

    try:
        return float(value)
    except ValueError:
        raise ValueError('{} is not a valid number.'.format(value))


def validate_request(request):

    start = _get_parameter(request, 'investmentDate')
    end = _get_parameter(request, 'currentDate')
    cdb = _get_parameter(request, 'cdbRate')

    start = _parse_date_format(start)
    end = _parse_date_format(end)
    cdb = _parse_float(cdb)

    return start, end, cdb
