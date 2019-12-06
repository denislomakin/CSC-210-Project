import random
from app import app, db
from app.forms import LoginForm, SignupForm, EventForm
from app.models import User,Event
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash,request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date,datetime
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import DateTimeField
from dateutil import parser


def flash_errors(form, type):
    for field, errors in form.errors.items():
        for error in errors:
            flash(type+error)


def get_event(eventId):
    return Event.query.filter_by(event_id=eventId).first()


eventPlaceholders = ["The Mad Hatter's Tea Party", 'Robanukah', 'Weasel Stomping Day', 'The Red Wedding', 'Scotchtoberfest', 'The Feast of Winter Veil', 'A Candlelit Dinner', 'Towel Day']
def render_home(page, event=None):
    return render_template('home.html', user=current_user, lform=LoginForm(), sform=SignupForm(), eform=EventForm(), eventPlaceholder=random.choice(eventPlaceholders), startPage=page, event=event)


@app.route('/')
def index():
    return render_home('createEventPage');


@app.route('/<int:eventId>')
def event():
    return render_home('viewEventPage', get_event(eventId))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('`Wrong Username or Password')
        else:
            login_user(user, remember=form.remember.data)
            return redirect('/')
    else:
        flash('`Wrong Username or Password')
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
        #     flash('`Username taken')
        #     return redirect('/')
        # if User.query.filter_by(email=form.email.data).first() is not None:
        #     flash('`That email is already associated with a MeetUp account.')
        #     return redirect('/')
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect('/')
    else:
        flash_errors(form, '`')
    return redirect('/')


anonymousNames = ['Willy Wonka', 'Darth Vader', 'Mary Poppins', 'John Connor', 'James Bond', 'Bruce Wayne', 'Peter Pan', 'Indiana Jones', 'Han Solo', 'Clark Kent', 'Ferris Bueller', 'Hannah Montana', 'Jon Snow', 'Jay Gatsby', 'Bruce Banner', 'Tony Stark', 'Ellen Ripley', 'Michael Scott', 'Steve Rogers', 'James T. Kirk']
@app.route('/createEvent', methods=['GET', 'POST'])
def createEvent():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(name=form.eventName.data, start=form.startTime.data, end=form.endTime.data, dates=form.dates.data, creator=(current_user.username if current_user.is_authenticated else random.choice(anonymousNames)), creatorId=(current_user.user_id if current_user.is_authenticated else 0))
        if current_user.is_authenticated:
            new_event.users.append(current_user)
        db.session.add(new_event)
        db.session.commit()
        flash('|'+form.eventName.data+' has been created with ID ' + str(new_event.event_id) + '.')
    else:
        flash_errors(form, '-')
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
