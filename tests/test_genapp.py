from x12genapp.genapp import (get_customers,
                              parse_genapp_customer)
from x12genapp.config import AppSettings
from x12genapp.x12.model import X12Demographics
import pytest
import json
import responses


@pytest.fixture
def app_settings() -> AppSettings:
    settings = AppSettings()
    # override defaults for test cases
    settings.genapp_customer_min_id = 1
    settings.genapp_customer_max_id = 2
    return settings


@pytest.fixture
def genapp_no_customer_match_response() -> bytes:
    """Returns a raw response where a customer lookup is not found"""
    return b'{"LGCMAREA":{"CA_REQUEST_SPECIFIC":"000","CA_CUSTOMER_REQUEST":{"CA_DOB":"","CA_FIRST_NAME":"","CA_POLICY_DATA":"","CA_LAST_NAME":"","CA_HOUSE_NAME":"","CA_NUM_POLICIES":0,"CA_HOUSE_NUM":"","CA_POSTCODE":""},"CA_RETURN_CODE":1,"CA_CUSTOMER_NUM":200}}'


@pytest.fixture
def genapp_first_customer_response() -> bytes:
    """Returns a matching customer lookup result"""
    return b'{"LGCMAREA":{"CA_REQUEST_SPECIFIC":"Andrew    Pandy               1950-07-11                    34  PI101OO 00007799 123456        01962 811234        A.Pandy@beebhouse.com","CA_CUSTOMER_REQUEST":{"CA_DOB":"1950-07-11","CA_FIRST_NAME":"Andrew","CA_POLICY_DATA":"07799 123456        01962 811234        A.Pandy@beebhouse.com","CA_LAST_NAME":"Pandy","CA_HOUSE_NAME":"","CA_NUM_POLICIES":0,"CA_HOUSE_NUM":"34","CA_POSTCODE":"PI101OO"},"CA_RETURN_CODE":0,"CA_CUSTOMER_NUM":1}}'


@pytest.fixture
def genapp_second_customer_response() -> bytes:
    """Returns a matching customer lookup result"""
    return b'{"LGCMAREA":{"CA_REQUEST_SPECIFIC":"Scott     Tracey              1965-09-30Tracey Island       1   TB14TV  000                    001 911911          REFROOM@TBHOLDINGS.COM","CA_CUSTOMER_REQUEST":{"CA_DOB":"1965-09-30","CA_FIRST_NAME":"Scott","CA_POLICY_DATA":"                    001 911911          REFROOM@TBHOLDINGS.COM","CA_LAST_NAME":"Tracey","CA_HOUSE_NAME":"Tracey Island","CA_NUM_POLICIES":0,"CA_HOUSE_NUM":"1","CA_POSTCODE":"TB14TV"},"CA_RETURN_CODE":0,"CA_CUSTOMER_NUM":2}}'


def test_parse_genapp_customer_no_match(genapp_no_customer_match_response):
    """Tests parse_genapp_customer where a match is not found"""
    unmatched_response = json.loads(genapp_no_customer_match_response)
    actual = parse_genapp_customer(unmatched_response)
    assert actual is None


def test_parse_genapp_customer_match(genapp_first_customer_response):
    """Tests parse_genapp_customer where a match is found"""
    expected = X12Demographics()
    expected.provenance_id = 1
    expected.first_name = 'ANDREW'
    expected.last_name = 'PANDY'
    expected.birth_date = '19500711'

    matched_response = json.loads(genapp_first_customer_response)
    actual = parse_genapp_customer(matched_response)

    assert expected.provenance_id == actual.provenance_id
    assert expected.first_name == actual.first_name
    assert expected.last_name == actual.last_name
    assert expected.birth_date == actual.birth_date


@responses.activate
def test_get_customers(genapp_first_customer_response,
                       genapp_second_customer_response,
                       app_settings,
                       monkeypatch):
    """Tests get_customers where two records are returned"""
    monkeypatch.setattr('x12genapp.genapp.get_app_settings', lambda: app_settings)

    lookup_url = f'{app_settings.genapp_base_url}{app_settings.genapp_customer_lookup}'
    responses.add(
        responses.GET,
        lookup_url + '/1',
        json=json.loads(genapp_first_customer_response)
    )

    responses.add(
        responses.GET,
        lookup_url + '/2',
        json=json.loads(genapp_second_customer_response)
    )

    actual = get_customers()

    assert len(actual) == 2
    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == lookup_url + '/1'
    assert responses.calls[1].request.url == lookup_url + '/2'
