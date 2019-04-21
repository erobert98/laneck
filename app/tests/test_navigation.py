def test_assert():
    assert True

def test_home_page(client):
  response = client.get('/')
  assert response.status_code == 200

