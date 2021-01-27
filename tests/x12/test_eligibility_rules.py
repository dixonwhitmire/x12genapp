from x12genapp.x12.rules.eligibility_rules import *
import pytest
from typing import Dict
from dataclasses import asdict

@pytest.fixture
def data_context() -> Dict:
    return {'is_subscriber': False, 'has_dependent': False}


@pytest.fixture
def data_cache() -> Dict:
    return {
        'subscriber': asdict(X12Demographics()),
        'dependent': asdict(X12Demographics())
    }


def test_parse_transaction_set():
    segment_data = ['ST', '270', '0001', '005010X279A1']
    data_context = {}
    data_cache = {}
    parse_transaction_set(segment_data, data_context, data_cache)

    assert data_context['is_subscriber'] is False
    assert data_context['has_dependent'] is False
    assert data_cache['subscriber'].keys() == asdict(X12Demographics()).keys()
    assert data_cache['dependent'].keys() == asdict(X12Demographics()).keys()


def test_parse_subscriber_hl_segment_no_dependent(data_context: Dict):
    segment_data = ['HL', '3', '2', '22', '0']
    parse_subscriber_hl_segment(segment_data, data_context, data_cache)
    assert data_context == {'is_subscriber': True, 'has_dependent': False}


def test_parse_subscriber_hl_segment_with_dependent(data_context: Dict):
    segment_data = ['HL', '3', '2', '22', '1']
    parse_subscriber_hl_segment(segment_data, data_context, data_cache)
    assert data_context == {'is_subscriber': True, 'has_dependent': True}


def test_parse_dependent_hl_segment(data_context: Dict, data_cache: Dict):
    data_context['is_subscriber'] = True
    data_context['has_dependent'] = True
    segment_data = ['HL', '4', '3', '23', '0']

    parse_dependent_hl_segment(segment_data, data_context, data_cache)
    assert data_context == {'is_subscriber': False, 'has_dependent': False}


def test_parse_subscriber_trn_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['TRN', '1', '1', '1453915417']
    data_context['is_subscriber'] = True

    parse_trn_segment(segment_data, data_context, data_cache)
    assert data_cache['subscriber']['trace_number'] == '1453915417'
    assert data_cache['dependent']['trace_number'] is None


def test_parse_dependent_trn_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['TRN', '1', '1', '1453915417']
    data_context['is_subscriber'] = False

    parse_trn_segment(segment_data, data_context, data_cache)
    assert data_cache['dependent']['trace_number'] == '1453915417'
    assert data_cache['subscriber']['trace_number'] is None


def test_parse_subscriber_nm1_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['NM1', 'IL', '1', 'DOE', 'JOHN', 'L', '', 'IV', 'MI', '11122333301']
    data_context['is_subscriber'] = True

    parse_nm1_segment(segment_data, data_context, data_cache)

    model = data_cache['subscriber']
    assert model['last_name'] == 'DOE'
    assert model['first_name'] == 'JOHN'
    assert model['middle_name'] == 'L'
    assert model['suffix'] == 'IV'
    assert model['identification_code_type'] == 'MI'
    assert model['identification_code'] == '11122333301'


def test_parse_dependent_nm1_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['NM1', '03', '1', 'DOE', 'JOHN', 'L', '', 'IV']
    data_context['is_subscriber'] = False

    parse_nm1_segment(segment_data, data_context, data_cache)

    model = data_cache['dependent']
    assert model['last_name'] == 'DOE'
    assert model['first_name'] == 'JOHN'
    assert model['middle_name'] == 'L'
    assert model['suffix'] == 'IV'


def test_parse_subscriber_group_number(data_context: Dict, data_cache: Dict):
    segment_data = ['REF', 'IL', '90210']
    data_context['is_subscriber'] = True

    parse_group_number(segment_data, data_context, data_cache)
    assert data_cache['subscriber']['group_number'] == '90210'


def test_parse_dependent_group_number(data_context: Dict, data_cache: Dict):
    segment_data = ['REF', 'IL', '90210']
    data_context['is_subscriber'] = False

    parse_group_number(segment_data, data_context, data_cache)
    assert data_cache['dependent']['group_number'] == '90210'


def test_parse_subscriber_n3_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['N3', '1400 Anywhere Lane', 'Apt 215']
    data_context['is_subscriber'] = True

    parse_n3_segment(segment_data, data_context, data_cache)
    model = data_cache['subscriber']
    assert model['address_line_1'] == '1400 Anywhere Lane'
    assert model['address_line_2'] == 'Apt 215'


def test_parse_dependent_n3_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['N3', '1400 Anywhere Lane', 'Apt 215']
    data_context['is_subscriber'] = False

    parse_n3_segment(segment_data, data_context, data_cache)
    model = data_cache['dependent']
    assert model['address_line_1'] == '1400 Anywhere Lane'
    assert model['address_line_2'] == 'Apt 215'


def test_parse_subscriber_n4_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['N4', 'Standards City', 'SC', '90210']
    data_context['is_subscriber'] = True

    parse_n4_segment(segment_data, data_context, data_cache)
    model = data_cache['subscriber']
    assert model['city'] == 'Standards City'
    assert model['state'] == 'SC'
    assert model['zip_code'] == '90210'


def test_parse_dependent_n4_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['N4', 'Standards City', 'SC', '90210']
    data_context['is_subscriber'] = False

    parse_n4_segment(segment_data, data_context, data_cache)
    model = data_cache['dependent']
    assert model['city'] == 'Standards City'
    assert model['state'] == 'SC'
    assert model['zip_code'] == '90210'


def test_parse_subscriber_dmg_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['DMG', 'D8', '19900515', 'F']
    data_context['is_subscriber'] = True

    parse_dmg_segment(segment_data, data_context, data_cache)
    model = data_cache['subscriber']
    assert model['birth_date'] == '19900515'
    assert model['gender'] == 'F'


def test_parse_dependent_dmg_segment(data_context: Dict, data_cache: Dict):
    segment_data = ['DMG', 'D8', '19900515', 'F']
    data_context['is_subscriber'] = False

    parse_dmg_segment(segment_data, data_context, data_cache)
    model = data_cache['dependent']
    assert model['birth_date'] == '19900515'
    assert model['gender'] == 'F'
