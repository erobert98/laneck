import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgres://lqwcftopfzmggv:f3c31ef8bfc07183d91284629f7ac9ea82d2711f9c44af7672a9ed0aecb4b574@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d1nq40njqg0fl'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'

class Testing(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgres://mostvftkkintch:aa584aafc230fdea601e382a5360d8dd81468b2041af23bd04fe3962c11839c8@ec2-54-225-113-7.compute-1.amazonaws.com:5432/dcv8jg8t9aedpn' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = False
    FLASK_ADMIN_SWATCH = 'cerulean'
