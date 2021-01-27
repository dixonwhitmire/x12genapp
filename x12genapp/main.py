from fastapi import FastAPI
from pydantic import BaseModel
from x12genapp.x12.parse import (create_271_message,
                                 parse)
from x12genapp.settings import Settings
from x12genapp.services import is_existing_member

settings = Settings()

app = FastAPI()


class X12RequestPayload(BaseModel):
    x12: str


class X12ResponsePayload(X12RequestPayload):
    x12_transaction_code: str


@app.post('/x12', response_model=X12ResponsePayload)
def post_x12(x12_payload: X12RequestPayload):
    """
    Posts a x12 eligibility transaction to the demo service, returning a 271
    response.
    """
    x12_demographics = parse(x12_payload.x12)
    is_existing_patient = True if settings.is_passthrough_enabled else is_existing_member(x12_demographics)

    response_data = {
        'x12_transaction_code': '271',
        'x12': create_271_message(x12_demographics, is_existing_patient)
    }

    x12_response = X12ResponsePayload(**response_data)
    return x12_response
