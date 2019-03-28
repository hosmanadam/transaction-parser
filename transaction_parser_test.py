import config
from transaction_parser import parse_transaction_body


CATEGORY_SHORTHANDS = ['groc', 'groceries', 'hyg', 'hygiene', 'clothes', 'eat', 'eating', 'eating out', 'tip']
# TODO: Pass shorthands_to_categories (built from database) for validation
# TODO: ...EXCEPT that would make testing harder so let's do that separately


fixtures = [

    {
        'inputs': [
            '1400+(2*400)huf istanbul kebab eating out  // transaction comment  # metacomment',
        ],
        'expected': [
            {
                'amount_hundredths': 220000,
                'currency_code': 'huf',
                'partner': 'istanbul kebab',
                'category': 'eating out',
                'transaction_comment': 'transaction comment',
                'metacomment': 'metacomment'
            },
        ]
    },

    {
        'inputs': [
            '14000-5000huf tgi fridays eating out of 3*1000 drinking out 1500 tip  // used amex, Amy chipped in',
        ],
        'expected': [
            {
                'amount_hundredths': 450000,
                'currency_code': 'huf',
                'partner': 'tgi fridays',
                'category': 'eating out',
                'transaction_comment': 'used amex, Amy chipped in',
                'metacomment': None
            },
            {
                'amount_hundredths': 300000,
                'currency_code': 'huf',
                'partner': 'tgi fridays',
                'category': 'drinking out',
                'transaction_comment': 'used amex, Amy chipped in',
                'metacomment': None
            },
            {
                'amount_hundredths': 150000,
                'currency_code': 'huf',
                'partner': 'tgi fridays',
                'category': 'tip',
                'transaction_comment': 'used amex, Amy chipped in',
                'metacomment': None
            },
        ]
    },

]


class TestParseTransactionBody:

    @staticmethod
    def run_it(fixture_index, input_index):
        parsed_transaction = parse_transaction_body(
            fixtures[fixture_index]['inputs'][input_index],
            CATEGORY_SHORTHANDS,
            config.ALL_CURRENCY_CODES
        )
        assert parsed_transaction == fixtures[fixture_index]['expected']

    def test_handles_body_without_exceptions(self):
        self.run_it(0, 0)

    def test_handles_body_with_exceptions(self):
        self.run_it(1, 0)
