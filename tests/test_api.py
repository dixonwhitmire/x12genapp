from x12genapp.app import app


def test_api():
    with app.test_client() as tc:
        response = tc.post('/genapp/x12')
        assert response.status_code == 200
