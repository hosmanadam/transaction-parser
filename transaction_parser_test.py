import config
from transaction_parser import parse_transaction_body


PARTNERS_TO_SHORTHANDS = {
    'ALDI': [],
    'Istanbul Kebab': ['ist', 'istanbul'],
    'Spotify': [],
    'TESCO': [],
    'TGI Fridays': ['tgi', 'fridays', 'tgifridays'],
    'Marks & Spencer': ['marks', 'ms'],
}

CATEGORIES_TO_SHORTHANDS = {
    'Clothes': [],
    'Drinking out': ['drink', 'drinking', 'drinkout', 'drinkingout'],
    'Eating out': ['eat', 'eatout', 'eating'],
    'Music': [],
    'Groceries': ['groc'],
    'Hygiene': ['hyg'],
    'Tip': [],
}


def swapparoo(full_to_short):
    """
    Return new dict which swaps keys & values of original, flattening all items of list values into individual keys

    - All keys are lowercase
    """
    short_to_full = {}
    for full, short_list in full_to_short.items():
        short_to_full.update({full.lower(): full})
        for short in short_list:
            short_to_full.update({short.lower(): full})
    return short_to_full


SHORTHANDS_TO_CATEGORIES = swapparoo(CATEGORIES_TO_SHORTHANDS)
SHORTHANDS_TO_PARTNERS = swapparoo(PARTNERS_TO_SHORTHANDS)


def mock_processed_transaction_body(
    amount_hundredths,
    currency_code,
    partner,
    category,
    transaction_comment=None,
    metacomment=None,
):
    return {
        'amount_hundredths': amount_hundredths,
        'currency_code': currency_code,
        'partner': partner,
        'category': category,
        'transaction_comment': transaction_comment,
        'metacomment': metacomment,
    }


# Just add fixtures, and they will be collected for testing
# Within one fixture, all inputs should result in the same output
FIXTURES = [

    {
        'inputs': [
            {'input_string': '900huf aldi groceries',
             'functionality': 'processes_transaction_in_lower_case'},
            {'input_string': '900HUF ALDI Groceries',
             'functionality': 'processes_transaction_in_mixed_case'},
            {'input_string': '   900huf   aldi      groceries',
             'functionality': 'ignores_extra_inline_whitespace'},
            {'input_string': '300 + 600huf aldi groceries',
             'functionality': 'handles_explicit_math'},
            {'input_string': '2*(150+300)huf aldi groceries',
             'functionality': 'handles_explicit_math_with_brackets'},
            {'input_string': '300 600huf aldi groceries',
             'functionality': 'handles_implicit_math'},
            # {'input_string': '900 aldi groceries',
            #  'functionality': 'gets_default_currency'},
            # {'input_string': '900huf aldi',
            #  'functionality': 'gets_default_category'},
            # {'input_string': '900huf aldi food',
            #  'functionality': 'figures_out_subcategory_from_category'},
        ],
        'expected': [
            mock_processed_transaction_body(90000, 'HUF', 'ALDI', 'Groceries'),
        ]
    },

    {
        'inputs': [
            {'input_string': '900huf aldi groceries  // duplicate?',
             'functionality': 'handles_transaction_comment'},
        ],
        'expected': [
            mock_processed_transaction_body(90000, 'HUF', 'ALDI', 'Groceries', 'duplicate?'),
        ]
    },

    {
        'inputs': [
            {'input_string': '4000huf aldi groc of 500 hygiene',
             'functionality': 'handles_single_category_exception'},
        ],
        'expected': [
            mock_processed_transaction_body(350000, 'HUF', 'ALDI', 'Groceries'),
            mock_processed_transaction_body(50000, 'HUF', 'ALDI', 'Hygiene'),
        ]
    },

    {
        'inputs': [
            {'input_string': '4000huf aldi groc of 500 hygiene 1000 clothes',
             'functionality': 'handles_multiple_category_exceptions'},
        ],
        'expected': [
            mock_processed_transaction_body(250000, 'HUF', 'ALDI', 'Groceries'),
            mock_processed_transaction_body(50000, 'HUF', 'ALDI', 'Hygiene'),
            mock_processed_transaction_body(100000, 'HUF', 'ALDI', 'Clothes'),
        ]
    },

    {
        'inputs': [
            {'input_string': '5eur spotify music',
             'functionality': 'handles_foreign_currency'},
        ],
        'expected': [
            mock_processed_transaction_body(500, 'EUR', 'Spotify', 'Music'),
        ]
    },

    {
        'inputs': [
            {'input_string': '4.99eur spotify music',
             'functionality': 'handles_foreign_currency_with_dot_decimal_separator'},
            {'input_string': '4,99eur spotify music',
             'functionality': 'handles_foreign_currency_with_comma_decimal_separator'},
        ],
        'expected': [
            mock_processed_transaction_body(499, 'EUR', 'Spotify', 'Music'),
        ]
    },

    {
        'inputs': [
            {'input_string': '12000huf aldi eating out',
             'functionality': 'handles_multiword_category'},
        ],
        'expected': [
            mock_processed_transaction_body(1200000, 'HUF', 'ALDI', 'Eating out'),
        ]
    },

    {
        'inputs': [
            {'input_string': '12000huf Marks & Spencer groceries',
             'functionality': 'handles_multiword_partner_name'},
            {'input_string': '12000huf marks groceries',
             'functionality': 'handles_shorthand_partner_name'},
            {'input_string': '12000huf Marks & Spencer groc',
             'functionality': 'handles_shorthand_category_name'},
        ],
        'expected': [
            mock_processed_transaction_body(1200000, 'HUF', 'Marks & Spencer', 'Groceries'),
        ]
    },

    {
        'inputs': [
            {'input_string': '14000-5000huf Tgi fridays eating out of 3*(400+600) drinking out 1500 tip  // used amex, Amy chipped in  # WOW',
             'functionality': 'integration_1'},
        ],
        'expected': [
            mock_processed_transaction_body(450000, 'HUF', 'TGI Fridays', 'Eating out', 'used amex, Amy chipped in', 'WOW'),
            mock_processed_transaction_body(300000, 'HUF', 'TGI Fridays', 'Drinking out', 'used amex, Amy chipped in', 'WOW'),
            mock_processed_transaction_body(150000, 'HUF', 'TGI Fridays', 'Tip', 'used amex, Amy chipped in', 'WOW'),
        ]
    },

]


class TestParseTransactionBody:

    @staticmethod
    def run_it(input, expected):
        parsed_transaction = parse_transaction_body(
            input,
            SHORTHANDS_TO_CATEGORIES,
            SHORTHANDS_TO_PARTNERS,
            config.ALL_CURRENCY_CODES,
        )
        assert parsed_transaction == expected

    for fixture in FIXTURES:
        for input in fixture['inputs']:
            exec(
                f"def test_{input['functionality']}(self):\n"
                f"    self.run_it(\n"
                f"        '{input['input_string']}',\n"
                f"        {fixture['expected']},\n"
                f"    )\n\n"
            )
