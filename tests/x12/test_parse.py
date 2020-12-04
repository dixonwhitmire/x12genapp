import pytest
from x12genapp.x12.model import X12Demographics
from x12genapp.x12.parse import parse


@pytest.fixture
def x12_demographics():
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


def test_parse(x12_message, x12_demographics):
    assert x12_demographics == parse(x12_message)
