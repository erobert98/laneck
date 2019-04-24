from app import app
from app.models import User
from flask import request
from flask_login import login_user, current_user

def test_uploadRequireLogin(client):
    with app.test_request_context():
        response = client.get('/upload') # this call shows the response object goes to login
        assert b'/login?next=%2Fupload' in response.data
 


# def test_uploadRequireAdmin(client):
#     with app.test_request_context():
#         U = User.query.filter_by(username ='admin').first()    
#         check = login_user(U, force=True)
#         UserCheck = current_user.username
#         response = client.get('/upload', follow_redirects=True)
#         assert request.endpoint == 'loign'
#         # var 