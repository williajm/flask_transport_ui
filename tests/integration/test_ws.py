import requests


def test_train_ws():
    resp = requests.get('http://127.0.0.1:5000')
    assert resp.status_code == requests.codes.ok
