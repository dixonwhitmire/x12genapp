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


class X12ResponsePayload(X12RequestPayload):
    """X12 response model - includes x12 response and transaction code"""
    x12_transaction_code: str


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
