from functools import lru_cache

import requests
from typing import (Dict,
                    Optional)
from x12genapp.x12.model import X12Demographics
from x12genapp.config import get_app_settings


def parse_genapp_customer(genapp_record: Dict) -> Optional[X12Demographics]:
    """
    Parses a GenApp Customer from a JSON response to a X12Demographics model
    :param genapp_record: The GenApp Customer record
    :return: The X12Demographics model for the customer record
    """
    no_match_found = genapp_record.get('LGCMAREA', {}).get('CA_RETURN_CODE', 1) == 1

    if no_match_found:
        return None

    provenance_id = genapp_record.get('LGCMAREA', {}).get('CA_CUSTOMER_NUM', -1)
    genapp_customer = genapp_record.get('LGCMAREA', {}).get('CA_CUSTOMER_REQUEST', {})

    data_fields = {
        'provenance_id': provenance_id,
        'first_name': genapp_customer.get('CA_FIRST_NAME', '').upper(),
        'last_name': genapp_customer.get('CA_LAST_NAME', '').upper(),
        'birth_date': genapp_customer.get('CA_DOB', '')
    }

    data_fields['birth_date'] = data_fields['birth_date'].replace('-', '')
    data_fields = {k: v for k, v in data_fields.items() if v != '' or v is not None}

    x12_demographics = X12Demographics(**data_fields)
    return x12_demographics


@lru_cache(maxsize=128)
def load_customers(endpoint_url: str, min_id: int, max_id: int) -> Dict:
    """
    Parses a range of genapp customer records using genapp record ids.
    :param endpoint_url: The GenApp endpoint used to lookup records.
    :param min_id: The minimum id in the range.
    :param max_id: The maximum id in the range
    :return: Dictionary of X12Demographic models indexed by hash
    """
    genapp_records = {}

    for i in range(min_id, max_id + 1, 1):

        response = requests.get(endpoint_url + '/' + str(i))
        if response.ok:
            response_data = response.json()
            x12_demographics = parse_genapp_customer(response_data)
            genapp_records[hash(x12_demographics)] = x12_demographics
        else:
            print(f'received a {response.status_code}: {response.text}')

    return genapp_records


def get_customers() -> Dict:
    """Returns a range of genapp customers indexed by hash"""
    settings = get_app_settings()
    lookup_url = f'{settings.genapp_base_url}{settings.genapp_customer_lookup}'
    return load_customers(lookup_url,
                          settings.genapp_customer_min_id,
                          settings.genapp_customer_max_id)
