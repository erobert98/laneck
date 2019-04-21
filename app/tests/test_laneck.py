import pytest
from conftest import client

def test_assert():
    assert True

def test_index(client):
    response = client.get('/index')
    assert response.status_code == 200
