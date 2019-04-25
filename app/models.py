from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import UserMixin, RoleMixin, login_required, current_user
from wtforms.fields import PasswordField

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def isAdminR(self):
        if self.name == 'admin':
            return True
        else:
            return False
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)   



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def isAdmin(self):
        if 'admin' in self.roles:
            return True
        else:  #weird that i need this but i guess its fine
            return False

    def __repr__(self):
        return '<User {}>'.format(self.username)   


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(140), index = True, unique=True)
    name = db.Column(db.String(130), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = db.backref('songs'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))