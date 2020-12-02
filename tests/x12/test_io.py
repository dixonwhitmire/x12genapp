import pytest
from x12genapp.x12.io import X12MessageDelimiters, X12Reader
from x12genapp.x12 import InvalidControlSegment


@pytest.fixture
def x12_message(scope='module'):
    return """ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~
GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~
ST*270*0001*005010X279A1~
BHT*0022*13*10001234*20200929*1319~
HL*1**20*1~
NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~
HL*2*1*21*1~
NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~
HL*3*2*22*0~
TRN*1*1*1453915417~
NM1*IL*1*DOE*JOHN****MI*11122333301~
DMG*D8*19800519~
DTP*291*D8*20200101~
EQ*30~
SE*13*0001~
GE*1*0001~
IEA*1*000010216~"""


def test_message_delimiters(x12_message):
    delimiters = X12MessageDelimiters(x12_message.replace('\n', ''))
    assert delimiters.element_separator == '*'
    assert delimiters.repetition_separator == '|'
    assert delimiters.segment_terminator == '~'


def test_message_delimiters_exception(x12_message):
    invalid_message = x12_message.replace('\n', '')[0:50]
    with pytest.raises(InvalidControlSegment):
        X12MessageDelimiters(invalid_message)


def test_message_reader(x12_message):
    reader = X12Reader(x12_message)
    assert reader.x12_delimiters.element_separator == '*'
    assert reader.x12_delimiters.repetition_separator == '|'
    assert reader.x12_delimiters.segment_terminator == '~'
    assert reader.transaction_code == '270'
    assert len(reader.x12_data) == 17
