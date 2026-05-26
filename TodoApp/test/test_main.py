from fastapi.testclient import TestClient
from .. import main
from fastapi import status


client = TestClient(main.app)

def test_return_health_check():
    response = client.get("/healthy")