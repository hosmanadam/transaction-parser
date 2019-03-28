import re

CHARSET_AMOUNT = '0123456789.,()+-*/ '


def process_currency_code(currency, currencies):
    """
    Validate and uppercase passed currency

    :param currency:
    :param currencies: List of valid currencies
    :return: Uppercased form of currency code, of `False` if code not valid
    """
    return currency.upper() if currency.upper() in currencies else False


def process_shorthand(shorthand, short_to_full):
    """
    Validate and complete passed shorthand

    :param shorthand:
    :param short_to_full: Dictionary of shorthand keys with corresponding complete values
    :return: Complete form of shorthand from passed dict, or `False` if shorthand not valid
    """
    return short_to_full[shorthand] if shorthand.lower() in short_to_full else False


def split_metacomment(rough_work):
    try:
        metacomment_start = rough_work.index('#')
        metacomment = rough_work[metacomment_start:].lstrip('# ')
        rough_work = rough_work[:metacomment_start].strip()
        return rough_work, metacomment
    except ValueError:
        return rough_work, None


def split_transaction_comment(rough_work):
    try:
        transaction_comment_start = rough_work.index('//')
        transaction_comment = rough_work[transaction_comment_start:].lstrip('/ ')
        rough_work = rough_work[:transaction_comment_start].strip()
        return rough_work, transaction_comment
    except ValueError:
        return rough_work, None


def split_amount(rough_work):
    i = 0
    while rough_work[i] in CHARSET_AMOUNT:
        i += 1
    amount_hundredths = eval(rough_work[:i])*100
    has_space_after_amount = rough_work[i-1] == ' '
    rough_work = rough_work[i:].strip()
    return rough_work, amount_hundredths, has_space_after_amount


def split_currency_code(rough_work, has_space_after_amount, all_currency_codes):
    currency_code = None
    if not has_space_after_amount:
        candidate = rough_work[:3]
        has_space_after_candidate = rough_work[3] == ' '
        if has_space_after_candidate:
            valid_candidate = process_currency_code(candidate, all_currency_codes)
            if valid_candidate:
                currency_code = valid_candidate
                rough_work = rough_work[3:].strip()
    return rough_work, currency_code


def split_exceptions(rough_work, shorthands_to_categories):
    try:
        exceptions_start = rough_work.index(' of ')
        exceptions = rough_work[exceptions_start:].replace(' of ', '').strip()
        exceptions = re.findall(r'(?P<amount>[\d\.\,\(\)\+\-\*\/ ]+)(?P<category>[a-zA-z ]+)', exceptions)
        exceptions = [{
            'amount_hundredths': eval(match[0])*100,
            'category': process_shorthand(match[1].strip(), shorthands_to_categories)
        } for match in exceptions]
        rough_work = rough_work[:exceptions_start].strip()
        excepted_amount_hundredths = sum(exception['amount_hundredths'] for exception in exceptions)
        return rough_work, exceptions, excepted_amount_hundredths
    except ValueError:
        return rough_work, [], 0


def split_category(rough_work, shorthands_to_categories):
    category = None
    if ' ' in rough_work:
        words = rough_work.split(' ')
        for i in range(len(words)-1, 0, -1):
            candidate = ' '.join(words[i:])
            valid_candidate = process_shorthand(candidate, shorthands_to_categories)
            if valid_candidate:
                category = valid_candidate
                rough_work = ' '.join(words[:i])
                break
    return rough_work, category


def parse_transaction_body(
    raw_transaction,
    shorthands_to_categories,
    all_currency_codes,
):
    """
    Split individual transaction string body into its component pieces (without header)

    - Takes some user & general datasets for disambiguation (not validation)

    :param raw_transaction:
    :param shorthands_to_categories:
    :param all_currency_codes:
    :return:
    """
    rough_work = raw_transaction.strip()
    rough_work = re.sub(' +', ' ', rough_work)
    rough_work, metacomment = split_metacomment(rough_work)
    rough_work, transaction_comment = split_transaction_comment(rough_work)
    rough_work, amount_hundredths, has_space_after_amount = split_amount(rough_work)
    rough_work, currency_code = split_currency_code(rough_work, has_space_after_amount, all_currency_codes)
    rough_work, exceptions, excepted_amount_hundredths = split_exceptions(rough_work, shorthands_to_categories)
    rough_work, category = split_category(rough_work, shorthands_to_categories)
    rough_work, partner = '', rough_work
    main_transaction = {
            'amount_hundredths': amount_hundredths - excepted_amount_hundredths,
            'currency_code': currency_code,
            'partner': partner,
            'category': category,
            'transaction_comment': transaction_comment,
            'metacomment': metacomment,
        }
    subtransactions = [{**main_transaction, **exception} for exception in exceptions]
    return [main_transaction, *subtransactions]
