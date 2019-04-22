from app.models import User
from flask_login import login_user
from app import app, db
from flask import url_for


def test_login(client):
    with app.test_request_context():
        U = User.query.first()
        login_user(U)
        print(U.email)
        response = client.get('/login')
        assert response.request.path == url_for('index')

