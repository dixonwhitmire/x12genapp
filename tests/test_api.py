import pytest
from tests import client
from x12genapp.config import (AppSettings, get_app_settings)
from x12genapp.x12.model import X12Demographics


@pytest.fixture
def app_settings() -> AppSettings:
    app_settings = AppSettings()
    return app_settings


def test_x12_post_passthrough(x12_270_basic_message: str,
                              x12_271_member_with_coverage_message: str,
                              app_settings: AppSettings):
    """tests /x12 [POST] where passthrough is enabled"""
    # override dependency
    app_settings.is_passthrough_enabled = True
    client.app.dependency_overrides[get_app_settings] = lambda: app_settings

    response = client.post('/x12', json={'x12': x12_270_basic_message})
    assert response.status_code == 200

    json_response = response.json()

    assert json_response['x12'] == x12_271_member_with_coverage_message
    assert json_response['x12_transaction_code'] == '271'

    client.app.dependency_overrides = {}


def test_x12_post_member_is_covered(x12_270_basic_message: str,
                                    x12_271_member_with_coverage_message: str,
                                    app_settings: AppSettings,
                                    x12_270_basic_demographics: X12Demographics,
                                    monkeypatch):
    """tests /x12 [POST] where a member has current coverage"""
    app_settings.is_passthrough_enabled = False
    client.app.dependency_overrides[get_app_settings] = lambda: app_settings

    hash_key = hash(x12_270_basic_demographics)
    monkeypatch.setattr('x12genapp.routes.x12.get_customers', lambda: {hash_key: x12_270_basic_demographics})

    response = client.post('/x12', json={'x12': x12_270_basic_message})
    assert response.status_code == 200

    json_response = response.json()
    assert json_response['x12'] == x12_271_member_with_coverage_message
    assert json_response['x12_transaction_code'] == '271'


def test_x12_post_member_is_not_covered(x12_270_basic_message: str,
                                        x12_271_member_not_found_message: str,
                                        app_settings: AppSettings,
                                        x12_270_basic_demographics: X12Demographics,
                                        monkeypatch):
    """tests /x12 [POST] where a member is not covered by the plan"""
    app_settings.is_passthrough_enabled = False
    client.app.dependency_overrides[get_app_settings] = lambda: app_settings

    monkeypatch.setattr('x12genapp.routes.x12.get_customers', lambda: {})

    response = client.post('/x12', json={'x12': x12_270_basic_message})
    assert response.status_code == 200

    json_response = response.json()
    assert json_response['x12'] == x12_271_member_not_found_message
    assert json_response['x12_transaction_code'] == '271'
