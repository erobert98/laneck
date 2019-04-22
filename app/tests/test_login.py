from app.models import User
from flask_login import login_user, current_user
from app import app, db
from flask import url_for, request


def test_login(client):
    with app.test_request_context():
        U = User.query.first()
        login_user(U)
        print(U.email)
        print(current_user.is_authenticated)
        response = client.get('/login')
        assert request.path == url_for('index')

