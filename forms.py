from flask_wtf import Form

from wtforms import StringField, PasswordField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)
from wtforms.fields.html5 import DateField
from datetime import date
from models import User

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class SignUpForm(Form):
	username = StringField(
			'Username',
			validators=[
				DataRequired(),
				Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
                ),
                name_exists
			]
		)

	email = StringField(
			'Email',
			validators=[
				DataRequired(),
				Email(),
				email_exists
			]
		)
	password = PasswordField(
			'Password',
			validators=[
				DataRequired(),
				Length(min=8),
				EqualTo('password2', 'Passwords must match!')
			]
		)
	password2 = PasswordField(
			'Confirm Password',
			validators=[
				DataRequired()
			]
		)

class LoginForm(Form):
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired()])

class TaskForm(Form):
	title = StringField('title', validators=[DataRequired()])
	content = TextAreaField('content')
	priority = SelectField('priority', choices=[('', 'Priority'), ('low','low'), ('medium', 'medium'), ('high','high')], default='Priority')
	date = DateField('Pick a Date')