from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Role
from werkzeug.urls import url_parse
from flask_login import logout_user, current_user, login_user, login_required
from flask_security import SQLAlchemyUserDatastore, roles_accepted



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
        login_user(user, remember=form.remember_me.data)
        flash(f'Sucessfully logged in {user.username}')
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



@app.before_first_request
def restrict_admin_url():
    endpoint = 'admin.index'
    url = url_for(endpoint)
    admin_index = app.view_functions.pop(endpoint)

    @app.route(url, endpoint=endpoint)
    @roles_accepted('admin')
    def secure_admin_index():
        return admin_index()