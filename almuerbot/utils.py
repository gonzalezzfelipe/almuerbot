import urllib.parse
from math import radians, sin, cos, acos, exp

import iso8601
from flask import request


def parse_args(decoding):
    """Parse request arguments using decoding dictionary."""
    return {
        k: request.args.get(k, type=v)
        for k, v in decoding.items() if request.args.get(k, type=v)
    }


def decode_url(encoded):
    """Decpde url string."""
    return urllib.parse.unquote(encoded)


def parse_datetime(date_string):
    """Parse string into datetime object.

    Uses ``iso8601.parse_date`` function to parse different formats.

    :param str date_string: Date in string format.
    :return: Datetime parsed from string or None.
    :rtype: datetime.datetime

    """
    return iso8601.parse_date(date_string)


def nullable_cast(type_):
    return lambda x: value if value is None else type_(value)


def ignore_empty_string(arg_type):
    """If request arg is an empty string, return empty string."""
    return lambda x: arg_type(x) if x != '' else x


def parse_from_env(value):
    """Parses boolean from environment."""
    value_lower = value.lower()
    if value_lower == 'true':
        return True
    elif value_lower == 'false':
        return False
    else:
        return value


def calculate_distance(start, end):
    slat, slon = radians(start[0]), radians(start[1])
    elat, elon = radians(end[0]), radians(end[1])
    return 6371.01 * acos(
        sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))


def sigmoid(x):
  return 1 / (1 + exp(-x))
