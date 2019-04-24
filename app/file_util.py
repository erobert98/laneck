from app import db  
from app.models import Song
from sqlalchemy.exc import IntegrityError


def store_fileInfo(filename, name, user):
    try:
        S = Song(location = filename, name = name, user_id = user)
        db.session.add(S)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False