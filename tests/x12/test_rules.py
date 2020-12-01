from x12genapp.x12.rules import load_rules, matches_segment


@matches_segment('HL', {3: '22'})
def hl_test_rule(segment_data, data_context, data_cache):
    """
    X12 test rule used to match to a HL subscriber segment:
    HL*3*2*22*1

    The rule sets an "is_executed" entry in the data_context, setting it to True
    :param segment_data: list of segment field values
    :param data_context: dictionary
    :param data_cache: dictionary
    """
    data_context['is_executed'] = True


def test_load_rules():
    rules = load_rules('270')
    assert len(rules) > 0


def test_rule_execution():
    segment_data = ['HL', '3', '2', '22', '1']
    data_context = {'is_executed': False}
    data_cache = {}
    hl_test_rule(segment_data, data_context, data_cache)
    assert data_context['is_executed'] is True

    segment_data[0] = 'FOO'
    data_context = {'is_executed': False}
    hl_test_rule(segment_data, data_context, data_cache)
    assert data_context['is_executed'] is False

    segment_data = ['HL', '3', '2', '23', '1']
    data_context = {'is_executed': False}
    hl_test_rule(segment_data, data_context, data_cache)
    assert data_context['is_executed'] is False
