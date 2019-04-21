import pytest
# from conftest import client 
from app import app


def test_assert():
    assert True

def test_home_page(client):
  response = client.get('/')
  assert response.status_code == 200

@pytest.fixture
def client():
  # app = Flask(__name__) 
  client = app.test_client()
  return client