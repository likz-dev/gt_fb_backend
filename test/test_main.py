import json


def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = {'status': 'ok'}
    assert json.loads(res.get_data(as_text=True)) == expected
