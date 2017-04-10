from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import URLField
from .models import User


class SigninForm(Form):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(Form):
    
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(3, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[ DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('Username already in use.') 




class AddFacilitator(Form):
    """Form to add facilitators to system"""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')
    




