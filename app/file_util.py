from app import db  
from app.models import Song
from sqlalchemy.exc import IntegrityError
import re



def store_fileInfo(fileLOC, name, user):
    try:
        # print(type(fileLOC))
        if ' ' in fileLOC:
            fileLOC = fileLOC.replace(' ','+')
        S = Song(location = fileLOC, name = name, user_id = user) #filename includes file extension
        print(S.location)
        db.session.add(S)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False