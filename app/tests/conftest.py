from app import app
import pytest 

@pytest.fixture
def client():
  # app = Flask(__name__) 
  client = app.test_client()
  return client