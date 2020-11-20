import pytest
from tests.fixture import eligibility_request
from x12genapp.x12.io import X12MessageDelimiters, X12Reader, InvalidControlSegment


def test_message_delimiters(eligibility_request):
    delimiters = X12MessageDelimiters(eligibility_request.replace('\n', ''))
    assert "*" == delimiters.element_separator
    assert "|" == delimiters.repetition_separator
    assert "~" == delimiters.segment_terminator


def test_message_delimiters_exception(eligibility_request):
    invalid_message = eligibility_request.replace('\n', '')[0:50]
    with pytest.raises(InvalidControlSegment):
        X12MessageDelimiters(invalid_message)


def test_message_reader(eligibility_request):
    reader = X12Reader(eligibility_request)
    assert "*" == reader.x12_delimiters.element_separator
    assert "|" == reader.x12_delimiters.repetition_separator
    assert "~" == reader.x12_delimiters.segment_terminator
    assert "270" == reader.transaction_code
    assert 17 == len(reader.x12_data)
