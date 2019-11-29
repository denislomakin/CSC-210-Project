from flask import flash, redirect
from flask_wtf import RecaptchaField, Recaptcha, FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64, message="Username must be between 4 and 64 characters long.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128, message="Password must be between 8 and 128 characters long.")])
    remember = BooleanField('Remember Me')


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=64, message="Email must be less than 64 characters.")])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=64, message="Username must be between 4 and 64 characters long.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128, message="Password must be between 8 and 128 characters long.")])
    password2 = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    recaptcha = RecaptchaField(validators=[Recaptcha(message="Recaptcha must be completed")])

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('Username taken')
            return redirect('/')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('That email is already associated with a MeetUp account.')
            return redirect('/')