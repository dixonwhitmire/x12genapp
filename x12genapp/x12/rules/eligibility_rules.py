from x12genapp.x12.rules import matches_segment
from x12genapp.x12.model import X12Demographics
from typing import (Dict,
                    List)
from dataclasses import asdict


@matches_segment('ST')
def parse_transaction_set(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a ST (transaction set) segment.
    Example: ST*270*0001*005010X279A1~
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    data_context['is_subscriber'] = False
    data_context['has_dependent'] = False
    data_cache['subscriber'] = asdict(X12Demographics())
    data_cache['dependent'] = asdict(X12Demographics())
    data_context['is_transaction_complete'] = False


@matches_segment('HL', {3: '22'})
def parse_subscriber_hl_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a HL (hierarchical level) Subscriber Segment:
    Example: HL*3*2*22*0
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    data_context['is_subscriber'] = True
    data_context['has_dependent'] = segment_data[4] == '1'


@matches_segment('HL', {3: '23'})
def parse_dependent_hl_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a HL (hierarchical level) Dependent Segment:
    Example: HL*3*2*23*0~
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    data_context['is_subscriber'] = False
    data_context['has_dependent'] = False


@matches_segment('TRN')
def parse_trn_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a TRN (trace number) segment:
    Example: TRN*1*1*1453915417~
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    model = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
    model['trace_number'] = segment_data[3]


@matches_segment('NM1')
def parse_nm1_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a NM1 (name) segment for a subscriber or dependent
    Example: NM1*IL*1*DOE*JOHN*L**IV*MI*11122333301~
    :param segment_data:
    :param data_context:
    :param data_cache:
    :return:
    """
    entity_id = segment_data[1]

    if entity_id.upper() not in ('IL', '03'):
        return

    model = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
    model['last_name'] = segment_data[3]
    model['first_name'] = segment_data[4]
    model['middle_name'] = segment_data[5]
    model['suffix'] = segment_data[7]

    if data_context['is_subscriber']:
        model['identification_code_type'] = segment_data[8]
        model['identification_code'] = segment_data[9]


@matches_segment('REF', {1: 'IL'})
def parse_group_number(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a REF segment used to convey the IL (group number) for the insured
    Example: REF*IL*90210~
    :param segment_data:
    :param data_context:
    :param data_cache:
    :return:
    """
    model = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
    model['group_number'] = segment_data[2]


@matches_segment('N3')
def parse_n3_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a N3 segment (address location)
    Example: N3*1400 Anywhere Lane*Apt 215~
    :param segment_data:
    :param data_context:
    :param data_cache:
    :return:
    """
    model = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
    model['address_line_1'] = segment_data[1]

    if len(segment_data) == 3:
        model['address_line_2'] = segment_data[2]


@matches_segment('N4')
def parse_n4_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a N4 segment (address geographic location)
    Example: N4*Standard City*SC*90210~
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    model = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
    model['city'] = segment_data[1]

    if len(segment_data) >= 3:
        model['state'] = segment_data[2]

    if len(segment_data) >= 4:
        model['zip_code'] = segment_data[3]


@matches_segment('DMG')
def parse_dmg_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses a DMG segment containing additional demographics (birth data and gender)
    Example: DMG*D8*19900515*F~
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    model = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']

    if len(segment_data) >= 3:
        model['birth_date'] = segment_data[2]

    if len(segment_data) >= 4:
        model['gender'] = segment_data[3]


@matches_segment('SE')
def parse_se_segment(segment_data: List, data_context: Dict, data_cache: Dict):
    """
    Parses
    :param segment_data:
    :param data_context:
    :param data_cache:
    """
    data_context['is_transaction_complete'] = True
