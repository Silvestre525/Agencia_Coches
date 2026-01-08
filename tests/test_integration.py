import httpx
import os
from os import getenv

def test_read_autos():
    base_url = os.getenv("TEST_URL","http://localhost:8000")
    url = f"{base_url}/api/autos/" 

    response = httpx.get(url)

    assert response.status_code == 200