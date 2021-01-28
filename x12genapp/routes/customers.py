from pydantic.main import BaseModel
from typing import List
from fastapi.routing import APIRouter
from fastapi import Depends
from x12genapp.config import AppSettings, get_app_settings
from x12genapp.genapp import get_customers

router = APIRouter()


class GenAppCustomer(BaseModel):
    """Response model for get all customers"""
    first_name: str
    last_name: str
    birth_date: str
    provenance_id: int


@router.get('', response_model=List[GenAppCustomer])
def get_all(app_settings: AppSettings = Depends(get_app_settings)):
    """Returns all "cached" customer records"""
    customer_response = []

    if app_settings.is_passthrough_enabled:
        return customer_response

    for k, v in get_customers().items():
        data_fields = {
            'first_name': v.first_name,
            'last_name': v.last_name,
            'birth_date': v.birth_date,
            'provenance_id': v.provenance_id
        }
        customer_response.append(GenAppCustomer(**data_fields))

    return customer_response
