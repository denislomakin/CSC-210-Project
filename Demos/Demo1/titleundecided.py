import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length,ValidationError, DataRequired, Email, EqualTo
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
appdir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'veryimportantsecret'
app.config["SQLALCHEMY_DATABASE_URI"] = \
    f"sqlite:///{os.path.join(appdir, 'users.db')}"

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UserEvents = db.Table('UserEvents',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
class Event(db.Model):
    id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    name = db.Column(db.String(256))
    start = db.Column(db.DateTime(), nullable=False)
    end = db.Column(db.DateTime(), nullable=False)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64, message="Username must be between 4 and 64 characters long.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128, message="Password must be between 8 and 128 characters long.")])
    remember = BooleanField('Remember Me')

class SignUpForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64, message="Email must be less than 64 characters.")])
    email2 = StringField('Retype Email Address', validators=[InputRequired(), Email(message='Invalid email'), EqualTo('email', message="Emails must match")])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64, message="Username must be between 4 and 64 characters long.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128, message="Password must be between 8 and 128 characters long.")])
    password2 = PasswordField(
        'Retype Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    

    def check_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def check_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % error)

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('personalpage'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('personalpage'))
        flash("Invalid Username or password")

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Username taken")
            return render_template('signup.html', form=form)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email already in use")
            return render_template('signup.html', form=form)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Your account has been created')
        return redirect(url_for('personalpage'))
    else:
        flash_errors(form)
    

    return render_template('signup.html', form=form)

@app.route('/personalpage')
@login_required
def personalpage():
    return render_template('personalpage.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
