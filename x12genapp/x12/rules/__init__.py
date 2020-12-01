from x12genapp.x12 import ELIGIBILITY_TRANSACTION_CODE
import importlib
import inspect
import functools

rule_modules = {
    ELIGIBILITY_TRANSACTION_CODE: 'eligibility_rules'
}


def matches_segment(segment_name, conditions=None):
    """
    Decorator used to match a x12 processing rule to a x12 segment.
    Matches are made by segment type with optional matching conditions.
    Matching conditions are limited to equality checks
    :param segment_name: The X12 segment name
    :param conditions: Dictionary of conditions. Key = x12 segment field index (zero based), Value = field value.
    :return: the decorated function
    """
    if conditions is None:
        conditions = {}

    def decorator(func):

        @functools.wraps(func)
        def wrapped(segment_data, data_context, data_cache):
            if segment_name.upper() == segment_data[0].upper():
                unmatched = {k: v for k, v in conditions.items() if segment_data[k].upper() != v.upper()}
                if len(unmatched) == 0:
                    func(segment_data, data_context, data_cache)
        return wrapped

    return decorator


def load_rules(transaction_code):
    """
    Loads processing rules for the specified x12 transaction
    :param transaction_code: the x12 transaction code
    :return:
    """
    rule_module_name = rule_modules.get(transaction_code)
    rule_module = importlib.import_module('x12genapp.x12.rules.' + rule_module_name)
    rules = inspect.getmembers(rule_module, inspect.isfunction)
    return rules
