from x12genapp.x12.rules import matches_segment


@matches_segment('ST')
def parse_transaction_set(segment_data, data_context, data_cache):
    """
    Parses a ST (transaction set) segment.
    Example: ST*270*0001*005010X279A1~
    :param segment_data:
    :param data_context:
    :param data_cache:
    :return:
    """
    data_context['is_subscriber'] = False
    data_cache['subscriber'] = None
    data_cache['dependent'] = None


@matches_segment('HL', {3: '22'})
def parse_subscriber_hl_segment(segment_data, data_context, data_cache):
    """
    Parses a HL Subscriber Segment:
    Example: HL*3*2*22*0
    :param segment_data: list of segment field values
    :param data_context: stores metadata used for processing
    :param data_cache: stores the current data record
    """
    data_context['is_subscriber'] = True
