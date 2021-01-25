import pytest
from x12genapp.x12.model import X12Demographics
from x12genapp.x12.parse import parse


@pytest.fixture
def x12_270_basic_demographics():
    record_fields = {
        'trace_number': '1453915417',
        'first_name': 'JOHN',
        'middle_name': None,
        'last_name': 'DOE',
        'suffix': None,
        'identification_code_type': 'MI',
        'identification_code': '11122333301',
        'birth_date': '19800519',
        'address_line_1': None,
        'address_line_2': None,
        'city': None,
        'state': None,
        'zip_code': None,
        'gender': None,
        'group_number': None
    }

    return X12Demographics(**record_fields)


@pytest.fixture
def x12_270_demographics_with_address():
    record_fields = {
        'trace_number': '1453915417',
        'first_name': 'JOHN',
        'middle_name': None,
        'last_name': 'DOE',
        'suffix': None,
        'identification_code_type': 'MI',
        'identification_code': '11122333301',
        'birth_date': '19800519',
        'address_line_1': '5150 ANYWHERE STREET',
        'address_line_2': 'APT 1B',
        'city': 'SOME CITY',
        'state': 'SC',
        'zip_code': '90210',
        'gender': 'M',
        'group_number': '500700'
    }

    return X12Demographics(**record_fields)


def test_parse_basic_demographics(x12_270_basic_message: str, x12_270_basic_demographics: str):
    assert parse(x12_270_basic_message) == x12_270_basic_demographics


def test_parse_demographics_with_address(x12_270_with_address_message: str, x12_270_demographics_with_address: str):
    assert parse(x12_270_with_address_message) == x12_270_demographics_with_address
