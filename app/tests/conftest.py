from app import app
import pytest 

@pytest.fixture
def client():
  client = app.test_client()
  return client

  
# def admin_login(client):
#     return client.post('/login', data=dict(
#         username='admin',
#         password='admin'
#     ), follow_redirects=True)
