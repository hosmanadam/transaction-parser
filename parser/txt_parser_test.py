from parser.txt_parser import parse_txt


# Just add fixtures, and they will be collected for testing
# Within one fixture, all inputs should result in the same output
FIXTURES = []


class TestParseTXT:

    @staticmethod
    def run_it(input, expected):
        parsed_txt = parse_txt(input)
        assert parsed_txt == expected

    for fixture in FIXTURES:
        for input in fixture['inputs']:
            exec(
                f"def test_{input['functionality']}(self):\n"
                f"    self.run_it(\n"
                f"        '{input['input_string']}',\n"
                f"        {fixture['expected']},\n"
                f"    )\n\n"
            )
