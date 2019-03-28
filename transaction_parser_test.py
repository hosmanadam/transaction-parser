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


def mock_single_transaction_body(
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
fixtures = [

    {
        'inputs': [
            '900HUF ALDI Groceries',                      # processes_transaction_in_varied_case
            '900huf aldi groceries',                      # processes_transaction_in_lower_case
            '   900huf   aldi      groceries',            # ignores_extra_inline_whitespace
            '900 ALDI Groceries',                         # adds_default_currency
            '900HUF ALDI',                                # adds_default_category
            '900HUF ALDI food',                           # figures_out_subcategory_from_category
            '300 + 600 ALDI Groceries',                   # handles_explicit_math
            '300 600 ALDI Groceries',                     # handles_implicit_math
        ],
        'expected': [
            mock_single_transaction_body(90000, 'HUF', 'ALDI', 'Groceries'),
        ]
    },

    {
        'inputs': [
            '1400+(2*400)huf istanbul kebab eating out  // transaction comment  # metacomment',  # handles_body_without_exceptions
        ],
        'expected': [
            {
                'amount_hundredths': 220000,
                'currency_code': 'HUF',
                'partner': 'Istanbul Kebab',
                'category': 'Eating out',
                'transaction_comment': 'transaction comment',
                'metacomment': 'metacomment'
            },
        ]
    },

    {
        'inputs': [
            '14000-5000huf tgi fridays eating out of 3*1000 drinking out 1500 tip  // used amex, Amy chipped in',  # handles_body_with_exceptions
        ],
        'expected': [
            {
                'amount_hundredths': 450000,
                'currency_code': 'HUF',
                'partner': 'TGI Fridays',
                'category': 'Eating out',
                'transaction_comment': 'used amex, Amy chipped in',
                'metacomment': None
            },
            {
                'amount_hundredths': 300000,
                'currency_code': 'HUF',
                'partner': 'TGI Fridays',
                'category': 'Drinking out',
                'transaction_comment': 'used amex, Amy chipped in',
                'metacomment': None
            },
            {
                'amount_hundredths': 150000,
                'currency_code': 'HUF',
                'partner': 'TGI Fridays',
                'category': 'Tip',
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
            SHORTHANDS_TO_CATEGORIES,
            SHORTHANDS_TO_PARTNERS,
            config.ALL_CURRENCY_CODES,
        )
        assert parsed_transaction == fixtures[fixture_index]['expected']

    # def test_processes_transaction_in_varied_case(self):
    #     self.run_it(0, 0)
    #
    # def test_processes_transaction_in_lower_case(self):
    #     self.run_it(0, 1)
    #
    # def test_ignores_extra_inline_whitespace(self):
    #     self.run_it(0, 2)
    #
    # def test_adds_default_currency(self):
    #     self.run_it(0, 3)
    #
    # def test_adds_default_category(self):
    #     self.run_it(0, 4)
    #
    # def test_figures_out_subcategory_from_category(self):
    #     self.run_it(0, 5)
    #
    # def test_handles_explicit_math(self):
    #     self.run_it(0, 6)
    #
    # def test_handles_implicit_math(self):
    #     self.run_it(0, 7)

    def test_handles_body_without_exceptions(self):
        self.run_it(1, 0)

    def test_handles_body_with_exceptions(self):
        self.run_it(2, 0)
