"""
global pytest fixture file
Fixtures defined in this file are available to all unit tests
"""
import pytest
from x12genapp.x12.model import X12Demographics
from typing import Dict
from dataclasses import asdict


@pytest.fixture
def x12_270_genapp_customer() -> str:
    """A x12 270 message with genapp customer demographics"""
    return '{"x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20200929*1319~HL*1**20*1~NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~HL*2*1*21*1~NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~HL*3*2*22*0~TRN*1*1*1453915417~NM1*IL*1*PUG*LOUIS****MI*11122333301~DMG*D8*1969-09-06~DTP*291*D8*20200101~EQ*30~SE*13*0001~GE*1*0001~IEA*1*000010216~"}'

@pytest.fixture
def x12_270_oneline_message() -> str:
    """A x12 270 transaction in one line without carriage returns/new line characters"""
    return '{"x12": "ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20200929*1319~HL*1**20*1~NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~HL*2*1*21*1~NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~HL*3*2*22*0~TRN*1*1*1453915417~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519~DTP*291*D8*20200101~EQ*30~SE*13*0001~GE*1*0001~IEA*1*000010216~"}'


@pytest.fixture
def x12_270_basic_message() -> str:
    """A X12 270 message with basic demographic fields, excluding address information"""
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
DMG*D8*19800519*M~
DTP*291*D8*20200101~
EQ*30~
SE*13*0001~
GE*1*0001~
IEA*1*000010216~""".replace('\n', '')


@pytest.fixture
def x12_270_with_address_message() -> str:
    """A X12 270 message with demographic fields including address information"""
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


@pytest.fixture
def x12_271_member_with_coverage_message() -> str:
    """A X12 271 message where the member has insurance coverage"""
    return 'ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*271*4321*005010X279A1~BHT*0022*11*10001234*20060501*1319~HL*1**20*1~NM1*PR*2*ABC COMPANY*****PI*842610001~HL*2*1*21*1~NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~HL*3*2*22*0~TRN*2*1453915417*9877281234~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519*M~DTP*346*D8*20060101~EB*1**30**GOLD 123 PLAN~EB*L~EB*1**1>33>35>47>86>88>98>AL>MH>UC~EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*10*****Y~EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*30*****N~LS*2120~NM1*P3*1*JONES*MARCUS****SV*0202034~LE*2120~SE*20*4321~'


@pytest.fixture
def x12_271_member_not_found_message() -> str:
    """A X12 271 message where the member is not found in the payer system and does not have insurance coverage"""
    return 'ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*271*4321*005010X279A1~BHT*0022*11*10001234*20060501*1319~HL*1**20*1~NM1*PR*2*ABC COMPANY*****PI*842610001~HL*2*1*21*1~NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~HL*3*2*22*0~TRN*2*1453915417*9877281234~NM1*IL*1*DOE*JOHN****MI*11122333301~DMG*D8*19800519*M~AAA*Y**75*C~SE*12*4321~'


@pytest.fixture
def x12_270_basic_demographics() -> X12Demographics:
    """A x12 demographics model which does not have address information"""
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
        'gender': 'M',
        'group_number': None
    }

    return X12Demographics(**record_fields)


@pytest.fixture
def x12_270_demographics_with_address() -> X12Demographics:
    """A x12 demographics model with address information"""
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


@pytest.fixture()
def x12_270_fields(x12_270_basic_demographics) -> Dict:
    """x12 demographics fields conveyed as a dictionary. Unused fields are set to empty strings"""
    data_fields = {k: '' if v is None else v for k, v in asdict(x12_270_basic_demographics).items()}
    return data_fields
