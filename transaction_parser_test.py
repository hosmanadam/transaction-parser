import config
from transaction_parser import parse_transaction_body


PARTNERS_TO_SHORTHANDS = {
    'ALDI': [],
    'TESCO': [],
    'Istanbul Kebab': ['ist', 'istanbul', 'kk', 'kalvin kebab'],
    'TGI Fridays': ['tgi', 'fridays', 'tgifridays'],
}

CATEGORIES_TO_SHORTHANDS = {
    'Clothes': [],
    'Drinking out': ['drink', 'drinking', 'drinkout', 'drinkingout'],
    'Eating out': ['eat', 'eatout', 'eating'],
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


# TODO: Build these from db, then scrap above
SHORTHANDS_TO_CATEGORIES = swapparoo(CATEGORIES_TO_SHORTHANDS)
SHORTHANDS_TO_PARTNERS = swapparoo(PARTNERS_TO_SHORTHANDS)


# Within one fixture, all inputs should result in the same output
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
