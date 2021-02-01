from pydantic.main import BaseModel
from fastapi.routing import APIRouter
from fastapi import Depends
from x12genapp.config import AppSettings, get_app_settings
from x12genapp.x12.parse import parse, create_271_message
from x12genapp.genapp import get_customers

router = APIRouter()


class X12RequestPayload(BaseModel):
    """X12 request model"""
    x12: str

    class Config:
        schema_extra = {
            'example': {
                'x12': 'ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*270*0001*005010X279A1~BHT*0022*13*10001234*20200929*1319~HL*1**20*1~NM1*PR*2*UNIFIED INSURANCE CO*****PI*842610001~HL*2*1*21*1~NM1*1P*2*DOWNTOWN MEDICAL CENTER*****XX*2868383243~HL*3*2*22*0~TRN*1*1*1453915417~NM1*IL*1*PUG*LOUIS****MI*11122333301~DMG*D8*1969-09-06~DTP*291*D8*20200101~EQ*30~SE*13*0001~GE*1*0001~IEA*1*000010216~'
            }
        }


class X12ResponsePayload(X12RequestPayload):
    """X12 response model - includes x12 response and transaction code"""
    x12_transaction_code: str

    class Config:
        schema_extra = {
            'example': {
                'x12': 'ISA*00*          *00*          *ZZ*890069730      *ZZ*154663145      *200929*1705*|*00501*000000001*0*T*:~GS*HS*890069730*154663145*20200929*1705*0001*X*005010X279A1~ST*271*4321*005010X279A1~BHT*0022*11*10001234*20060501*1319~HL*1**20*1~NM1*PR*2*ABC COMPANY*****PI*842610001~HL*2*1*21*1~NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~HL*3*2*22*0~TRN*2*1453915417*9877281234~NM1*IL*1*PUG*LOUIS****MI*11122333301~DMG*D8*1969-09-06*~DTP*346*D8*20060101~EB*1**30**GOLD 123 PLAN~EB*L~EB*1**1>33>35>47>86>88>98>AL>MH>UC~EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*10*****Y~EB*B**1>33>35>47>86>88>98>AL>MH>UC*HM*GOLD 123 PLAN*27*30*****N~LS*2120~NM1*P3*1*JONES*MARCUS****SV*0202034~LE*2120~SE*20*4321~',
                'x12_transaction_code': '271'
            }
        }


@router.post('', response_model=X12ResponsePayload)
def post_x12(x12_payload: X12RequestPayload,
             app_settings: AppSettings = Depends(get_app_settings)):
    """Posts a x12 eligibility transaction to the demo service, returning a 271 response."""
    x12_demographics = parse(x12_payload.x12)
    has_coverage = True

    if not app_settings.is_passthrough_enabled:
        lookup_key = hash(x12_demographics)
        has_coverage = lookup_key in get_customers()

    response_data = {
        'x12_transaction_code': '271',
        'x12': create_271_message(x12_demographics, has_coverage)
    }

    x12_response = X12ResponsePayload(**response_data)
    return x12_response
