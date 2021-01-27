from x12genapp.x12.parse import parse


def test_parse_basic_demographics(x12_270_basic_message: str, x12_270_basic_demographics: str):
    assert parse(x12_270_basic_message) == x12_270_basic_demographics


def test_parse_demographics_with_address(x12_270_with_address_message: str, x12_270_demographics_with_address: str):
    assert parse(x12_270_with_address_message) == x12_270_demographics_with_address
