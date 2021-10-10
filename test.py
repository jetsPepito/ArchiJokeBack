from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_all_jokes():
    response = client.get("/jokes")
    assert response.status_code == 200
    assert response.json() == [{
    "_id": "6162ece2abd02b50766c244d",
    "title": "Une bonne blague",
    "body": "Sah quel plaisir",
    "date": "2021-09-01T22:00:00+00:00",
    "likes": 12,
    "dislikes": 5,
    "author": "Louis"
  }]