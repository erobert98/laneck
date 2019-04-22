def test_assert():
    assert True

def test_home_page(client):
  response = client.get('/index')
  assert response.status_code == 200

def test_login(client):
  response = client.get('/login')
  assert response.status_code == 200

def test_logout(client):  #redirect from logout when not logged in
  response = client.get('/logout')
  assert response.status_code == 302


def test_fail(client):
  response = client.get('/12321')
  assert response.status_code == 404
  