import re


# TRANSACTION HEADER

CHARSET_DATETIME_DELIMITERS = r'.-:'
RE_ANY_WHITESPACE = r' +'
RE_DELIMITING_WHITESPACE = r'(?<=[\d])(?P<delimiting_whitespace> +)(?=[\d])'
RE_LATITUDE = r'(?P<latitude>\d{1,2}\.\d{,8})'
RE_LONGITUDE = r'(?P<longitude>\d{1,3}\.\d{,8})'
RE_COORDINATES = (
    rf'at \('
    rf'{RE_LATITUDE}'
    rf', '
    rf'{RE_LONGITUDE}'
    rf'\)'
)
RE_DATETIME = r'[\d]{4}(?:\. |-)[\d\.\-\: ]*'
RE_DATETIME_DELIMITERS = r'\.|\-|\:'


# TRANSACTION BODY

CHARSET_AMOUNT = '0123456789.,()+-*/ '
RE_MULTIPLE_WHITESPACES = r' {2,}'
RE_IMPLICIT_ADDITION_SPACE = r'(?<=[\d)]) +(?=[\d(])'
RE_CATEGORY_EXCEPTION = r'(?P<amount>[\d\.\,\(\)\+\-\*\/\% ]+)(?P<category>[a-zA-z ]+)'


# ENTRY

RE_LOOKBEHIND_LINEBREAK_OR_START_OF_STRING = r'(?:(?<=\n)|(?<=^))'
RE_NONCAPTURING_LINEBREAK_OR_END_OF_STRING = r'(?:\n|$)'
RE_MULTILINE_WHATEVER_LAZY = rf'[\s\S]*?'
RE_LOOKAHEAD_ANY_WHITESPACE_AND_DATETIME_OR_END_OF_STRING = (
    rf'(?='
    rf'\s*'
    rf'{RE_DATETIME}'
    rf'|'
    rf'\s*$'
    rf')'
)

RE_ENTRY = (
    rf'{RE_LOOKBEHIND_LINEBREAK_OR_START_OF_STRING}'
    rf'(?P<entry>'
    rf'{RE_DATETIME}'
    rf'{RE_MULTILINE_WHATEVER_LAZY}'
    rf')'
    rf'{RE_LOOKAHEAD_ANY_WHITESPACE_AND_DATETIME_OR_END_OF_STRING}'
)
