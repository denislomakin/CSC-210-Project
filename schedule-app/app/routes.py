from app import app
from app.forms import LoginForm, SignupForm
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(128))


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % error)

@app.route('/')
def index():
    return render_template('home.html', user=current_user, lform=LoginForm(), sform=SignupForm())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect('/')
    else:
        flash('Wrong username or password')
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        if User.query.filter_by(username=form.username.data).first() is not None:
            flash('Username taken')
            return redirect('/')
        if User.query.filter_by(email=form.email.data).first() is not None:
            flash('That email is already associated with a MeetUp account.')
            return redirect('/')
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect('/')
    else:
        flash_errors(form)
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')