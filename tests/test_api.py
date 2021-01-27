from tests import client
from x12genapp import main
from x12genapp.main import settings


def test_x12_post_member_is_covered(x12_270_basic_message: str,
                                    x12_271_member_with_coverage_message: str,
                                    monkeypatch):
    monkeypatch.setattr(settings, 'is_passthrough_enabled', True)
    response = client.post('/x12', json={'x12': x12_270_basic_message})
    assert response.status_code == 200

    json_response = response.json()

    assert json_response['x12'] == x12_271_member_with_coverage_message
    assert json_response['x12_transaction_code'] == '271'


def test_x12_post_member_is_not_covered(x12_270_basic_message: str,
                                        x12_271_member_not_found_message: str,
                                        monkeypatch):
    monkeypatch.setattr(main, 'is_existing_member', lambda x: False)
    response = client.post('/x12', json={'x12': x12_270_basic_message})
    assert response.status_code == 200

    json_response = response.json()

    assert json_response['x12'] == x12_271_member_not_found_message
    assert json_response['x12_transaction_code'] == '271'
