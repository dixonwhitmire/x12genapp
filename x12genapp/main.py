from fastapi import FastAPI
from pydantic import BaseModel
from x12genapp.x12.parse import (create_271_message,
                                 parse)


app = FastAPI()


class X12RequestPayload(BaseModel):
    x12: str


class X12ResponsePayload(X12RequestPayload):
    x12_transaction_code: str


@app.post('/x12', response_model=X12ResponsePayload)
def post_x12(x12_payload: X12RequestPayload):
    x12_demographics = parse(x12_payload.x12)

    response_data = {
        'x12': create_271_message(x12_demographics),
        'x12_transaction_code': '271'
    }

    x12_response = X12ResponsePayload(**response_data)
    return x12_response
