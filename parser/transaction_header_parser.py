import re
from datetime import datetime

from parser.exceptions import *

CHARSET_DATETIME_DELIMITERS = r'.-:'
RE_ANY_WHITESPACE = r' *'
RE_DELIMITING_WHITESPACE = re.compile(r'(?<=[\d])(?P<delimiting_whitespace> +)(?=[\d])')
RE_COORDINATES = re.compile(
    r'at \('
    r'(?P<latitude>\d{1,2}\.\d{,8})'
    r', '
    r'(?P<longitude>\d{1,3}\.\d{,8})'
    r'\)'
)
RE_DATETIME = re.compile(r'^[\d]{4}[\d\.\-\: ]*')
RE_DATETIME_DELIMITERS = re.compile(r'\.|\-|\:')


def extract_coordinates(raw_header):
    match = re.findall(RE_COORDINATES, raw_header)
    if match:
        latitude = float(match[0][0])
        longitude = float(match[0][1])
        coordinates = {'latitude': latitude, 'longitude': longitude}
    else:
        coordinates = None
    return coordinates


def extract_datetime_object(raw_header):
    datetime_values = re.match(RE_DATETIME, raw_header).group()
    datetime_values = re.sub(RE_DELIMITING_WHITESPACE, '.', datetime_values)
    datetime_values = re.sub(RE_ANY_WHITESPACE, '', datetime_values)
    datetime_values = datetime_values.strip(CHARSET_DATETIME_DELIMITERS)
    datetime_values = re.split(RE_DATETIME_DELIMITERS, datetime_values)
    datetime_values = [int(value) for value in datetime_values]
    while len(datetime_values) < 3:
        datetime_values.append(1)
    return datetime(*datetime_values)


def parse_transaction_header(raw_header):
    try:
        datetime_object = extract_datetime_object(raw_header)
        coordinates = extract_coordinates(raw_header)
        return {'datetime': datetime_object, 'coordinates': coordinates}
    except Exception as e:
        print(f"Can't process '{raw_header}':\n{e}")
