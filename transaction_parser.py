import re

CHARSET_AMOUNT = '0123456789.,()+-*/ '


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
        if candidate.upper() in all_currency_codes and has_space_after_candidate:
            currency_code = candidate
            rough_work = rough_work[3:].strip()
    return rough_work, currency_code


def split_exceptions(rough_work, category_shorthands):
    try:
        exceptions_start = rough_work.index(' of ')
        exceptions = rough_work[exceptions_start:].replace(' of ', '').strip()
        exceptions = re.findall(r'(?P<amount>[\d\.\,\(\)\+\-\*\/ ]+)(?P<category>[a-zA-z ]+)', exceptions)
        exceptions = [{'amount_hundredths': eval(match[0])*100, 'category': match[1].strip()} for match in exceptions]
        rough_work = rough_work[:exceptions_start].strip()
        excepted_amount_hundredths = sum(exception['amount_hundredths'] for exception in exceptions)
        return rough_work, exceptions, excepted_amount_hundredths
    except ValueError:
        return rough_work, None


def split_category(rough_work, category_shorthands):
    category = None
    if ' ' in rough_work:
        words = rough_work.split(' ')
        for i in range(len(words)-1, 0, -1):
            candidate = ' '.join(words[i:])
            if candidate in category_shorthands:
                category = candidate
                rough_work = ' '.join(words[:i])
    return rough_work, category


def parse_transaction_body(
    raw_transaction,
    category_shorthands,
    all_currency_codes,
):
    """
    Split individual transaction string body into its component pieces (without header)

    :param raw_transaction:
    :param category_shorthands:
    :param all_currency_codes:
    :return:
    """
    rough_work = raw_transaction.strip()
    rough_work = re.sub(' +', ' ', rough_work)
    rough_work, metacomment = split_metacomment(rough_work)
    rough_work, transaction_comment = split_transaction_comment(rough_work)
    rough_work, amount_hundredths, has_space_after_amount = split_amount(rough_work)
    rough_work, currency_code = split_currency_code(rough_work, has_space_after_amount, all_currency_codes)
    rough_work, exceptions, excepted_amount_hundredths = split_exceptions(rough_work, category_shorthands)
    rough_work, category = split_category(rough_work, category_shorthands)
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
