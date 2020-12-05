"""
global pytest fixture file
Fixtures defined in this file are available to all unit tests
"""
import pytest

@pytest.fixture
def x12_270_oneline_message():
    return '{"x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20200929*1319~HL*1**20*1~NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~HL*2*1*21*1~NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~HL*3*2*22*0~TRN*1*1*1453915417~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519~DTP*291*D8*20200101~EQ*30~SE*13*0001~GE*1*0001~IEA*1*000010216~"}'


@pytest.fixture
def x12_270_basic_message():
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
IEA*1*000010216~""".replace('\n', '')


@pytest.fixture
def x12_270_with_address_message():
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
REF*IL*500700~
N3*5150 ANYWHERE STREET*APT 1B~
N4*SOME CITY*SC*90210~
DMG*D8*19800519*M~
DTP*291*D8*20200101~
EQ*30~
SE*13*0001~
GE*1*0001~
IEA*1*000010216~""".replace('\n', '')
