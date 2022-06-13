from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from src.main import app
from src.depends.auth import set_valid_credentials

client = TestClient(app)


def test_api_security():
    # no auth header
    resp = client.get('/api/v1/lcdman/1')
    assert resp.status_code == 401

    # invalid auth credentials
    auth = HTTPBasicAuth(username="invalid", password="pass")
    resp = client.get('/api/v1/lcdman/1', auth=auth)
    assert resp.status_code == 401

    # valid auth credentials
    set_valid_credentials('testuser', 'testpass')
    auth = HTTPBasicAuth(username="testuser", password="testpass")
    resp = client.get('/api/v1/lcdman/1', auth=auth)
    assert resp.status_code == 200

def test_set_lcd_page():
    set_valid_credentials('testuser', 'testpass')
    auth = HTTPBasicAuth(username="testuser", password="testpass")

    body = "1\t2\n3\t4"
    resp = client.post('/api/v1/lcdman/1', auth=auth, json={"body": body})
    assert resp.status_code == 200

