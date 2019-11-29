import random
from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import User
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % error)


eventPlaceholders = ["The Mad Hatter's Tea Party", 'Robanukah', 'Weasel Stomping Day', 'The Red Wedding', 'Scotchtoberfest', 'The Feast of Winter Veil', 'A Candlelit Dinner', 'Towel Day', ]
@app.route('/')
def index():
    return render_template('home.html', user=current_user, lform=LoginForm(), sform=SignupForm(), eventPlaceholder=random.choice(eventPlaceholders))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Wrong Username or Password')
        else:
            login_user(user, remember=form.remember.data)
            return redirect('/')
    else:
        flash('Wrong username or password')
    return redirect('/')

@app.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
    return render_template('scheduler.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        # if User.query.filter_by(username=form.username.data).first() is not None:
        #     flash('Username taken')
        #     return redirect('/')
        # if User.query.filter_by(email=form.email.data).first() is not None:
        #     flash('That email is already associated with a MeetUp account.')
        #     return redirect('/')
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect('/')
    else:
        flash_errors(form)
    return redirect('/')


@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
