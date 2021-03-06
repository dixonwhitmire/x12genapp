from x12genapp.x12.rules import (load_rules,
                                 transaction_rules)
from x12genapp.x12.model import X12Demographics
from dataclasses import asdict


def test_load_rules():
    rules = load_rules('270')
    assert 'ST' in rules
    assert len(rules['ST']) > 0

    assert 'HL' in rules
    assert len(rules['HL']) > 0


def test_matched_rule_execution():
    segment_data = ['ST', '270', '0001', '005010X279A1']
    data_context = {}
    data_cache = {}
    st_rule = transaction_rules['270']['ST'][0]
    st_rule(segment_data, data_context, data_cache)
    assert data_context['is_subscriber'] is False
    x12_demographics = asdict(X12Demographics())
    assert data_cache['subscriber'].keys() == x12_demographics.keys()
    assert data_cache['dependent'].keys() == x12_demographics.keys()


def test_unmatched_rule_execution():
    segment_data = ['FOO', '270', '0001', '005010X279A1']
    data_context = {}
    data_cache = {}
    st_rule = transaction_rules['270']['ST'][0]
    st_rule(segment_data, data_context, data_cache)
    assert 'is_subscriber' not in data_context
    assert 'subscriber' not in data_cache
    assert 'dependent' not in data_cache
