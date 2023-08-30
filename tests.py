import pytest
import httpx
from app import app



def test_get_index():
    with httpx.Client(app=app, base_url="http://127.0.0.1:5000") as client:
        r = client.get("/")
        assert r.status_code == 200


def test_shorten_url():
    with httpx.Client(app=app, base_url="http://127.0.0.1:5000") as client:
        data = {
            "long_url": "https://www.python-httpx.org/quickstart/",
            "expiration_date": "2023-08-29"
        }
        r = client.post("/", json=data)
        assert r.status_code == 200


def test_shorten_url_is_invalid():
    with httpx.Client(app=app, base_url="http://127.0.0.1:5000") as client:
        data = {
            "long_url": "https://www.../",
            "expiration_date": "2023-08-29"
        }
        r = client.post("/", json=data)
        assert r.status_code == 400
        assert r.json() == {"message": "Invalid url"}
    


