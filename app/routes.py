from flask import render_template, flash, redirect, request, url_for, send_from_directory
from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm
from app.models import User, Role, Post, Song
from werkzeug.urls import url_parse
from flask_login import logout_user, current_user, login_user, login_required
from flask_security import SQLAlchemyUserDatastore, roles_accepted
from werkzeug.utils import secure_filename
import math
import os
from functools import wraps
from app.file_util import store_fileInfo


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print(current_user)
            if current_user.isAdmin() is False:
                flash("That page requires admin access")
                return render_template('index.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper

@app.before_first_request
def before_first_request():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')
    db.session.commit()

@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template('index.html', title = "Welcome to Atlantic Beats")
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data, force=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/posts', methods=['GET', 'POST'])
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page, 10, False)
    P = Post.query.count()
    last_page = math.ceil(int(P) / int(10))
    print(last_page)
    page_url = "url_for('music', page="
    next_url = url_for('posts', page=posts.next_num) \
      if posts.has_next else None
    prev_url = url_for('posts', page=posts.prev_num) \
      if posts.has_prev else None

    return render_template('posts.html', confirmed_posts = P, posts = posts.items, cols =['Song Name'], page = page, next_url=next_url, prev_url=prev_url, last_page=last_page)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def upload_file():
    print(current_user.roles) #returns either admin or end-user but next line always goes through?
    # if current_user.roles is 'admin':
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    form = UploadForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        name = request.form['text']
        user = current_user.id
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            flash('Unsupported File Type')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if store_fileInfo(filename, name, user): #creates db entry for song e
                print('succesful upload')
                return redirect(url_for('music'))
            else:
                flash('Song already exists in the database')
                return redirect(request.url)
    return render_template('upload.html', form = form)

    
@app.route('/music')
@login_required
def music():
    page = request.args.get('page', 1, type=int)
    songs = Song.query.paginate(page, 10, False)
    P = Song.query.count()
    last_page = math.ceil(int(P) / int(10))
    print(last_page)
    page_url = "url_for('music', page="
    next_url = url_for('music', page=songs.next_num) \
      if songs.has_next else None
    prev_url = url_for('music', page=songs.prev_num) \
      if songs.has_prev else None

    return render_template('music.html', confirmed_songs = P, songs = songs.items, page = page, next_url=next_url, prev_url=prev_url, last_page=last_page, cols = ['Song Name', '', 'Contact Address'])
        
@app.route('/music/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in (app.config['ALLOWED_EXTENSIONS'])


