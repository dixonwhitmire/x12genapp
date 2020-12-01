from x12genapp.x12.rules import load_rules, transaction_rules


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
    assert data_cache['subscriber'] is None
    assert data_cache['dependent'] is None


def test_unmatched_rule_execution():
    segment_data = ['FOO', '270', '0001', '005010X279A1']
    data_context = {}
    data_cache = {}
    st_rule = transaction_rules['270']['ST'][0]
    st_rule(segment_data, data_context, data_cache)
    assert 'is_subscriber' not in data_context
    assert 'subscriber' not in data_cache
    assert 'dependent' not in data_cache
