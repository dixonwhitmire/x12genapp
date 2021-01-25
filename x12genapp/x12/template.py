from typing import Dict


def get_271_response_existing_member(demographics: Dict) -> str:
    """
    Returns an Eligibility/271 response where a member has current insurance coverage.
    :param demographics: Demographic fields included within the x12 response.
    """
    x12 = f"""ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~
GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~
ST*271*4321*005010X279A1~
BHT*0022*11*10001234*20060501*1319~
HL*1**20*1~
NM1*PR*2*ABC COMPANY*****PI*842610001~
HL*2*1*21*1~
NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~
HL*3*2*22*0~
TRN*2*{demographics['trace_number']}*9877281234~
NM1*IL*1*{demographics['last_name']}*{demographics['first_name']}*{demographics['middle_name']}***{demographics['identification_code_type']}*{demographics['identification_code']}~
DMG*D8*{demographics['birth_date']}*{demographics['gender']}~
DTP*346*D8*20060101~
EB*1**30**GOLD 123 PLAN~
EB*L~
EB*1**1>33>35>47>86>88>98>AL>MH>UC~
EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*10*****Y~
EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*30*****N~
LS*2120~
NM1*P3*1*JONES*MARCUS****SV*0202034~
LE*2120~
SE*20*4321~""".replace('\n', '')
    return x12


def get_271_response_member_not_found(demographics: Dict) -> str:
    """
    Returns an Eligibility/271 response where a member is not found.
    :param demographics: Demographic fields included within the x12 response.
    :return: x12 transaction
    """
    x12 = f"""ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~
GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~
ST*271*4321*005010X279A1~
BHT*0022*11*10001234*20060501*1319~
HL*1**20*1~
NM1*PR*2*ABC COMPANY*****PI*842610001~
HL*2*1*21*1~
NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~
HL*3*2*22*0~
TRN*2*{demographics['trace_number']}*9877281234~
NM1*IL*1*{demographics['last_name']}*{demographics['first_name']}*{demographics['middle_name']}***{demographics['identification_code_type']}*{demographics['identification_code']}~
DMG*D8*{demographics['birth_date']}*{demographics['gender']}~
AAA*Y**75*C~
SE*12*4321~""".replace('\n', '')
    return x12

