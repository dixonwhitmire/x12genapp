from x12genapp.x12.io import X12Reader
from x12genapp.x12.rules import load_rules
from x12genapp.x12.model import X12Demographics


def parse(x12_message):
    """
    Parses a X12 message into a demographic data structure
    :param x12_message: The x12 message payload
    :return: demographics as a X12Demographics named tuple
    """
    x12_reader = X12Reader(x12_message)
    parsing_rules = load_rules(x12_reader.transaction_code)

    x12_demographics = None
    data_context = {'is_transaction_complete': False}
    data_cache = {}

    for segment_fields in x12_reader.read_segment():
        if len(segment_fields) == 0:
            continue

        for rule in parsing_rules.get(segment_fields[0], []):
            rule(segment_fields, data_context, data_cache)

        if data_context['is_transaction_complete']:
            data_record = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
            data_record = {k: None if not v else v for k, v in data_record.items() }
            x12_demographics = X12Demographics(**data_record)
            break

    return x12_demographics
