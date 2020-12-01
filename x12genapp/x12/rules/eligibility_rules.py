from x12genapp.x12.rules import matches_segment


@matches_segment('HL', {3: '22'})
def parse_subscriber_hl_segment(segment_data, data_context, data_cache):
    """
    Parses a HL7 Subscriber Segment:
    HL*3*2*22*0
    :param segment_data: list of segment field values
    :param data_context: stores metadata used for processing
    :param data_cache: stores the current data record
    """
    data_context['is_subscriber'] = True
    data_context['has dependent'] = segment_data[4] == '1'

    data_cache['subscriber'] = None

    if data_context['has_dependent']:
        data_cache['dependent'] = None
