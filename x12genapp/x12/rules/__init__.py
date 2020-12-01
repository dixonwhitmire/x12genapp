from x12genapp.x12 import ELIGIBILITY_TRANSACTION_CODE
import importlib
import inspect
import functools
import collections


def matches_segment(segment_name, conditions=None):
    """
    Decorator used to match a x12 processing rule to a x12 segment.
    Matches are made by segment type with optional matching conditions.
    Matching conditions are limited to equality checks.
    The wrapped function is updated to include a segment_grouping attribute equal to the segment_name.
    :param segment_name: The X12 segment name
    :param conditions: Dictionary of conditions. Key = x12 segment field index (zero based), Value = field value.
    :return: the decorated function
    """
    if conditions is None:
        conditions = {}

    def decorator(func):
        func.segment_grouping = segment_name.upper()

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
    :return: defaultdict(list) mapping segment names to the list of rules (functions)
    """
    rule_module_name = rule_modules.get(transaction_code)
    rule_module = importlib.import_module('x12genapp.x12.rules.' + rule_module_name)
    rules = inspect.getmembers(rule_module, inspect.isfunction)
    filtered_rules = [rule for (name, rule) in rules if hasattr(rule, 'segment_grouping')]

    grouped_rules = collections.defaultdict(list)
    for rule in filtered_rules:
        grouped_rules[rule.segment_grouping].append(rule)
    return grouped_rules


# maps a x12 transaction code to the module containing the rules
rule_modules = {
    ELIGIBILITY_TRANSACTION_CODE: 'eligibility_rules'
}

# maps a x12 transaction code to the rules for that transaction set
# key = transaction code
# value = dict containing segment type/group -> rule functions
transaction_rules = {
    ELIGIBILITY_TRANSACTION_CODE: load_rules(ELIGIBILITY_TRANSACTION_CODE)
}
