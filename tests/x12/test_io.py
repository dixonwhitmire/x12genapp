import pytest
from x12genapp.x12.io import (X12MessageDelimiters,
                              X12Reader)
from x12genapp.x12 import (InvalidControlSegment,
                           InvalidEnvelope)


def test_message_delimiters(x12_270_basic_message: str):
    delimiters = X12MessageDelimiters(x12_270_basic_message.replace('\n', ''))
    assert delimiters.element_separator == '*'
    assert delimiters.repetition_separator == '|'
    assert delimiters.segment_terminator == '~'


def test_message_delimiters_exception(x12_270_basic_message: str):
    invalid_message = x12_270_basic_message.replace('\n', '')[0:50]
    with pytest.raises(InvalidControlSegment):
        X12MessageDelimiters(invalid_message)


def test_message_reader(x12_270_basic_message: str):
    reader = X12Reader(x12_270_basic_message)
    assert reader.x12_delimiters.element_separator == '*'
    assert reader.x12_delimiters.repetition_separator == '|'
    assert reader.x12_delimiters.segment_terminator == '~'
    assert reader.transaction_code == '270'
    assert len(reader.x12_data) == 17


def test_message_reader_invalid_envelope(x12_270_basic_message: str):
    invalid_message = x12_270_basic_message.replace('~ST*', '')
    with pytest.raises(InvalidEnvelope):
        X12Reader(invalid_message)

