from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_incident():
    res = client.post("/incidents/", json={"severity":3,"description":"dark lane feels unsafe","lat":27.19,"lng":88.50,"consent_public_map":True})
    assert res.status_code == 200
    assert res.json()["ok"] is True