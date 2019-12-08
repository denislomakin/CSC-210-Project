import random
from app import app, db
from app.forms import LoginForm, SignupForm, EventForm,RequestResetForm, ResetPasswordForm,InviteToEventForm
from app.models import User,Event
from app.scheduler import Schedule
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash,request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date,datetime
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import DateTimeField
from dateutil import parser
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.parse
import urllib.request
import json
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html
import smtplib

eventPlaceholders = ["The Mad Hatter's Tea Party", 'Robanukah', 'Weasel Stomping Day', 'The Red Wedding', 'Scotchtoberfest', 'The Feast of Winter Veil', 'A Candlelit Dinner', 'Towel Day', ]

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
GOOGLE_CLIENT_ID = '570974553537-v4mr65mlcjp966q8iq75qkc7g8btusu9.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'GpqWDz9qqxg9ncVd_zp_Lrsm'
GOOGLE_REFRESH_TOKEN = '1//0dUmDbXVDnrOGCgYIARAAGA0SNwF-L9IrVmfXprmu_GxgL8mbwfNPCi5anBdmW7SVmN6w-v0hId-5sBWWPF0ZTiOJ26G2b09uogA'


def flash_errors(form, type):
    for field, errors in form.errors.items():
        for error in errors:
            flash(type+error)


def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string

def command_to_url(command):
    return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)


def call_refresh_token(client_id, client_secret, refresh_token):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['refresh_token'] = refresh_token
    params['grant_type'] = 'refresh_token'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)

def refresh_authorization(google_client_id, google_client_secret, refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret, refresh_token)
    return response['access_token'], response['expires_in']


def send_mail(fromaddr, toaddr, subject, message):

    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, access_token, as_base64=True)

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    part_text = MIMEText(lxml.html.fromstring(message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
    part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
    msg_alternative.attach(part_text)
    msg_alternative.attach(part_html)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()
def get_event(eventId):
    return Event.query.filter_by(event_id=eventId).first()


eventPlaceholders = ["The Mad Hatter's Tea Party", 'Robanukah', 'Weasel Stomping Day', 'The Red Wedding', 'Scotchtoberfest', 'The Feast of Winter Veil', 'A Candlelit Dinner', 'Towel Day']
def render_home(page, event=None):
    return render_template('home.html', user=current_user, lform=LoginForm(), sform=SignupForm(), eform=EventForm(), pform=RequestResetForm(), eventPlaceholder=random.choice(eventPlaceholders), startPage=page, event=event)


@app.route('/')
def index():
    return render_home('createEventPage');


@app.route('/<int:eventId>')
def event(eventId):
    if current_user.is_authenticated:
        event=get_event(eventId)
        event.users.append(current_user)
        db.session.commit()
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

@app.route('/scheduler/<int:eventId>', methods=['GET', 'POST'])
def scheduler(eventId):
    return render_template('scheduler.html', schedule=Schedule(get_event(eventId)))


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
        flash('~Account ' + form.username.data + ' Created.')
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
    return redirect(url_for('invite',eventId=new_event.event_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/invite/<int:eventId>",methods=['GET', 'POST'])
def invite(eventId):
    
    form=InviteToEventForm()
    if form.validate_on_submit():
        event=get_event(eventId)
        email=form.email.data
        send_mail('meetupeasyschedule@gmail.com',email, event.name, f'''You have been invited to {event.name}. Follow url to schedule the event:
        {url_for('event', eventId=eventId, _external=True)}
        ''')
        flash('~Invitation Email Sent.')
        return redirect('/')
    else:
          flash_errors(form, '`')
    return render_template('invite.html', title='Invite to Event', form=form)
    
        

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect('/')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        send_mail('meetupeasyschedule@gmail.com', user.email, 'Reset Password', f'''Click the following link to reset your password:
        {url_for('reset_token', token=token, _external=True)}
        ''')
        flash('~Password Reset Email Sent.')
        return redirect('/')
    else:
        flash_errors(form, '`')
    return redirect('/')

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect('/')
    user = User.verify_reset_token(token)
    if user is None:
        flash('-That is an invalid or expired token')
        return redirect('/')
    print(user.username)
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('|Your password has been updated.')
        return redirect('/')
    return render_template('reset_token.html', title='Reset Password', form=form)
