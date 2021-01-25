from x12genapp.x12.io import X12Reader
from x12genapp.x12.rules import load_rules
from x12genapp.x12.model import X12Demographics

from typing import Tuple


def parse(x12_message: str) -> Tuple:
    """
    Parses a X12 message into a demographic data structure
    :param x12_message: The x12 message payload
    :return: demographics as a X12Demographics named tuple
    """
    x12_reader = X12Reader(x12_message)
    parsing_rules = load_rules(x12_reader.transaction_code)

    x12_demographics = None
    data_context = {'is_transaction_complete': False}
    data_cache = {}

    for segment_fields in x12_reader.read_segment():
        if len(segment_fields) == 0:
            continue

        for rule in parsing_rules.get(segment_fields[0], []):
            rule(segment_fields, data_context, data_cache)

        if data_context['is_transaction_complete']:
            data_record = data_cache['subscriber'] if data_context['is_subscriber'] else data_cache['dependent']
            data_record = {k: None if not v else v for k, v in data_record.items() }
            x12_demographics = X12Demographics(**data_record)
            break

    return x12_demographics


def create_271_message(x12_demographics: Tuple) -> str:
    """
    Creates a 271 message by applying x12 demographics to a template
    :param x12_demographics
    :return: x12 message
    """
    data = x12_demographics._asdict()
    data = {k: '' if v is None else v for k, v in data.items()}

    address_lines = ''
    address_location = ''
    if data['address_line_1']:
        address_lines = f"N3*{data['address_line_1']}*{data['address_line_2']}~"
        address_location = f"N4*{data['address_city']}*{data['state']}*{data['zip_code']}~"

    additional_demographics = ''
    if data['birth_date'] or data['gender']:
        additional_demographics = f"DMG*D8*{data['birth_date']}*{data['gender']}~"

    return f"""ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~
GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~
ST*271*4321*005010X279A1~
BHT*0022*11*10001234*20060501*1319~
HL*1**20*1~
NM1*PR*2*ABC COMPANY*****PI*842610001~
HL*2*1*21*1~
NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~
HL*3*2*22*0~
TRN*2*{data['trace_number']}*9877281234~
NM1*IL*1*{data['last_name']}*{data['first_name']}*{data['middle_name']}***{data['identification_code_type']}*{data['identification_code']}~
{address_lines}
{address_location}
{additional_demographics}
DTP*346*D8*20060101~
EB*1**30**GOLD 123 PLAN~
EB*L~
EB*1**1>33>35>47>86>88>98>AL>MH>UC~
EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*10*****Y~
EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*30*****N~
LS*2120~
NM1*P3*1*JONES*MARCUS****SV*0202034~
LE*2120~
SE*22*4321~""".replace('\n', '')
