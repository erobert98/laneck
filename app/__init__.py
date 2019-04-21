from flask import Flask
from config import Config, Testing
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sslify import SSLify
from flask_login import LoginManager
import os

app = Flask(__name__)
Bootstrap(app)
# sslify = SSLify(app)
app.config.from_object(Testing)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models