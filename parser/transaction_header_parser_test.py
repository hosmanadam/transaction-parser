from parser.transaction_header_parser import parse_transaction_header
import datetime


def mock_processed_transaction_header(datetime_values, coordinates=None):
    return {
        'datetime': datetime.datetime(*datetime_values),
        'latitude': coordinates[0] if coordinates else None,
        'longitude': coordinates[1] if coordinates else None,
    }


FIXTURES = [

    {
        'inputs': [
            {'input_string': '2019. 11. 11. 11:11:11 at (47.486671, 19.048319)',
             'functionality': 'handles_full_time_accuracy'},
        ],
        'expected': mock_processed_transaction_header((2019, 11, 11, 11, 11, 11), (47.486671, 19.048319)),
    },

]


class TestParseTransactionHeader:

    @staticmethod
    def run_it(input, expected):
        parsed_transaction_header = parse_transaction_header(input)
        assert parsed_transaction_header == expected

    for fixture in FIXTURES:
        for input in fixture['inputs']:
            exec(
                f"def test_{input['functionality']}(self):\n"
                f"    self.run_it(\n"
                f"        '{input['input_string']}',\n"
                f"        {fixture['expected']},\n"
                f"    )\n\n"
            )
