from app.forms import RegistrationForm
from app import app, db
from wtforms import ValidationError
import pytest
from app.models import User


def test_sameEmail(client):
    with app.test_request_context():
        with pytest.raises(ValidationError):
                form = RegistrationForm(username = 'admin', email = 'admin@admin.com', password = 'admin', password2 = 'admin', submit = True )
                print(form.email.data)
                form.validate_email(form.email)


def test_sameUser(client):
    with app.test_request_context():
        with pytest.raises(ValidationError):
                form = RegistrationForm(username = 'admin', email = 'admin@admin.com', password = 'admin', password2 = 'admin', submit = True )
                print(form.username.data)
                form.validate_username(form.username)

def test_sendUserInfo(client):
        U = User(email = 'test', username = 'test', password_hash = 'test')
        db.session.add(U)
        db.session.commit()
        user = User.query.filter_by(username = 'test').first()
        assert user is not None
        db.session.delete(user)
        db.session.commit()