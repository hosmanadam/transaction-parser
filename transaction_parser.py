import re


def parse_transaction_body(
    raw_transaction,
    category_shorthands,
    all_currency_codes,
):
    """
    Split and process individual transaction string body (without header)

    :param raw_transaction:
    :param category_shorthands:
    :param all_currency_codes:
    :return:
    """

    rough_work = raw_transaction

    # Remove consecutive whitespaces
    rough_work = re.sub(' +', ' ', rough_work)

    # Break off metacomment
    try:
        meta_comment_start = rough_work.index('#')
        meta_comment = rough_work[meta_comment_start:].strip()
        rough_work = rough_work[:meta_comment_start].strip()
    except ValueError:
        pass
    # TODO: strip comment characters

    # Break off transaction_comment
    try:
        transaction_comment_start = rough_work.index('//')
        transaction_comment = rough_work[transaction_comment_start:].strip()
        rough_work = rough_work[:transaction_comment_start].strip()
    except ValueError:
        pass
    # TODO: strip comment characters

    # Break off amount
    i = 0
    while rough_work[i] in '0123456789.,()+-*/ ':
        i += 1
    amount = eval(rough_work[:i])
    has_space_after_amount = rough_work[i-1] == ' '
    rough_work = rough_work[i:].strip()
    # TODO: convert to hundredths

    # Break off currency code
    currency_code = None
    if not has_space_after_amount:
        candidate = rough_work[:3]
        has_space_after_candidate = rough_work[3] == ' '
        if candidate.upper() in all_currency_codes and has_space_after_candidate:
            currency_code = candidate
            rough_work = rough_work[3:].strip()

    # Break off category
    category = None
    if ' ' in rough_work:
        words = rough_work.split(' ')
        for i in range(len(words)-1, 0, -1):
            candidate = ' '.join(words[i:])
            if candidate in category_shorthands:
                category = candidate
                rough_work = ' '.join(words[:i])

    # Break off partner
    partner = rough_work

    return {
        'amount': amount,
        'currency_code': currency_code,
        'partner': partner,
        'category': category,
        'transaction_comment': transaction_comment,
        'meta_comment': meta_comment,
    }
