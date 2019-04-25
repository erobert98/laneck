import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgres://lqwcftopfzmggv:f3c31ef8bfc07183d91284629f7ac9ea82d2711f9c44af7672a9ed0aecb4b574@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d1nq40njqg0fl'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    ALLOWED_EXTENSIONS = set(['mp3','wav'])
    S3_BUCKET                 = 'laneck'
    # S3_KEY                    = 'AKIAJRUHIPGPLFV56AVQ'
    # S3_SECRET                 = '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'
    S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")

class Testing(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgres://mostvftkkintch:aa584aafc230fdea601e382a5360d8dd81468b2041af23bd04fe3962c11839c8@ec2-54-225-113-7.compute-1.amazonaws.com:5432/dcv8jg8t9aedpn' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    ALLOWED_EXTENSIONS = set(['mp3', 'wav'])
    PRESERVE_CONTEXT_ON_EXCEPTION  = True
    S3_BUCKET                 = 'laneck'
    # S3_KEY                    = 'AKIAJRUHIPGPLFV56AVQ'
    # S3_SECRET                 = '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'
    S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")

