from x12genapp.x12.io import X12Reader
from x12genapp.x12.rules import load_rules
from x12genapp.x12.model import X12Demographics
from x12genapp.x12.template import (get_271_existing_member,
                                    get_271_member_not_found)

from typing import Tuple


def parse(x12_message: str) -> X12Demographics:
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


def create_271_message(x12_demographics: X12Demographics, is_existing_member: bool) -> str:
    """
    Creates a 271 message by applying x12 demographics to a template
    :param x12_demographics
    :param is_existing_member
    :return: x12 message
    """
    data = x12_demographics._asdict()
    data = {k: '' if v is None else v for k, v in data.items()}

    if is_existing_member:
        return get_271_existing_member(data)

    return get_271_member_not_found(data)
